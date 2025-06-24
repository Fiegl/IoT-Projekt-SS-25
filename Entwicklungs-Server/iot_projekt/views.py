import json, csv
import uuid
from django.shortcuts import render, redirect
from django.http import HttpResponse, JsonResponse
from django.contrib.auth.hashers import make_password, check_password
from django.core.mail import send_mail                                      #wird f�r Passwort zur�cksetzen ben�tigt
from functools import wraps                                                 #wird f�r den Decorator ben�tigt
from django.views.decorators.cache import never_cache                       #verhindert den Cache
from datetime import datetime
from django.contrib import messages
from django.views.decorators.http import require_GET

#from .led_control import set_led_status
#from .tageslichtsensor import start_sensor, stop_sensor, get_luxwert



# Pfad zu den JSON-Datenbanken

registrierte_benutzer = "/var/www/django-project/datenbank/users.json"
reset_tokens = "/var/www/django-project/datenbank/reset_tokens.json"
arbeitsplaetze = "/var/www/django-project/datenbank/arbeitsplaetze.json"
rechnungsbelege = "/var/www/django-project/datenbank/rechnungsbelege.json"

#Hier ist die Funktion f�r den Decorator
def login_required(view_func):
    @wraps(view_func)
    def wrapper(request, *args, **kwargs):
        if not request.session.get("username"):
            return redirect("start")
        return view_func(request, *args, **kwargs)
    return wrapper
    
@never_cache
def registrieren(request):
    if request.method == "POST":
        username = request.POST.get("username")
        email = request.POST.get("email")
        password = request.POST.get("passwort")

        with open(registrierte_benutzer, "r") as file:
            data = json.load(file)

        if any(user["username"] == username for user in data["users"]):
            return HttpResponse("Benutzername bereits vergeben.")

        koerpergroesse = int(request.POST.get("koerpergroeße"))
        new_user = {
            "id": str(uuid.uuid4()),
            "username": username,
            "email": email,
            "password": make_password(password),
            "koerpergroesse": koerpergroesse
        }

        data["users"].append(new_user)

        with open(registrierte_benutzer, "w") as file:
            json.dump(data, file, indent=4)

        return redirect("start")

    return render(request, 'iot_projekt/registrieren.html')
    
@never_cache
def start(request):
    if request.method == "POST":
        username = request.POST.get("username")
        password = request.POST.get("passwort")

        with open(registrierte_benutzer, "r") as file:
            data = json.load(file)

        for user in data["users"]:
            if user["username"] == username and check_password(password, user["password"]):
      
                request.session["username"] = username
                request.session["user_id"] = user["id"]

                return redirect("hauptseite")

        return HttpResponse("Ihr Passwort oder Benutzername ist falsch, bitte erneut eingeben.")

    return render(request, 'iot_projekt/start.html')


@never_cache
@login_required
def logout_view(request):
    request.session.flush()
    return redirect("start")

def berechne_schreibtischhoehe(koerpergroesse_cm):
    return round(koerpergroesse_cm * 0.4)

    
    
#Hier sind die Funktionen f�r das Passwort zur�cksetzen (SMTP GMAIL, siehe settings.py)


def load_reset_tokens():
    try:
        with open(reset_tokens, "r") as f:
            return json.load(f)
    except FileNotFoundError:
        return {}
    except json.JSONDecodeError:
        return {}

def save_reset_tokens(tokens):
    with open(reset_tokens, "w") as f:
        json.dump(tokens, f, indent=4)


def passwort_vergessen(request):
    if request.method == "POST":
        email = request.POST.get("email")

        with open(registrierte_benutzer, "r") as file:
            data = json.load(file)

        for user in data["users"]:
            if user["email"] == email:
                token = str(uuid.uuid4())
                tokens = load_reset_tokens()
                tokens[token] = user["username"]
                save_reset_tokens(tokens)

                reset_link = request.build_absolute_uri(f"/passwort_zuruecksetzen/{token}/")

                send_mail(
                    'Passwort zur�cksetzen � Desk-Share-Lock',
                    f'Hallo {user["username"]},\n\nHier ist dein Link:\n{reset_link}',
                    'deinemail@gmail.com',
                    [email],
                    fail_silently=False,
                )

                return HttpResponse("E-Mail wurde versendet.")
        
        return HttpResponse("E-Mail nicht gefunden.")

    return render(request, 'iot_projekt/passwort_vergessen.html')
    
    
    
    
def passwort_zuruecksetzen(request, token):
    tokens = load_reset_tokens()
    username = tokens.get(token)

    if not username:
        return HttpResponse("Ung�ltiger oder abgelaufener Link.")

    if request.method == "POST":
        neues_passwort = request.POST.get("passwort")
        neues_hash = make_password(neues_passwort)

        with open(registrierte_benutzer, "r") as file:
            data = json.load(file)

        for user in data["users"]:
            if user["username"] == username:
                user["password"] = neues_hash
                break

        with open(registrierte_benutzer, "w") as file:
            json.dump(data, file, indent=4)

        # Token l�schen
        del tokens[token]
        save_reset_tokens(tokens)

        return HttpResponse("Passwort erfolgreich ge�ndert!")

    return render(request, 'iot_projekt/passwort_zuruecksetzen.html', {"token": token})



#Hier die Funktion f�r die MainPage
@never_cache
@login_required
def hauptseite(request):
    if "username" not in request.session:
        return redirect("start")

    with open(arbeitsplaetze, "r") as file:
        arbeitsplaetze_data = json.load(file)["arbeitsplaetze"]

    with open(registrierte_benutzer, "r") as file:
        users = json.load(file)["users"]

    user_id = request.session.get("user_id")
    schreibtischhoehe = None

    # Mapping von user_id zu username vorbereiten
    user_map = {user["id"]: user["username"] for user in users}

    # Benutzernamen zuordnen und Tischhöhe berechnen
    for arbeitsplatz in arbeitsplaetze_data:
        uid = arbeitsplatz.get("user_id")
        if uid:
            arbeitsplatz["username"] = user_map.get(uid, "Unbekannt")

        if uid == user_id and schreibtischhoehe is None:
            for user in users:
                if user["id"] == user_id:
                    schreibtischhoehe = berechne_schreibtischhoehe(user.get("koerpergroesse", 170))
                    break

    return render(request, 'iot_projekt/mainpage.html', {
        "arbeitsplaetze_list": arbeitsplaetze_data,
        "arbeitsplaetze_json": json.dumps(arbeitsplaetze_data),
        "user_id": user_id,
        "schreibtischhoehe": schreibtischhoehe
    })




@require_GET                #hier haben wir ein REST-API:-)
@login_required
def luxwert_aktuell(request):
    user_id = request.session.get("user_id")

    with open(arbeitsplaetze, "r") as file:
        daten = json.load(file)

    for ap in daten["arbeitsplaetze"]:
        if ap.get("user_id") == user_id and ap.get("status") == "belegt":
            ap_id = ap["id"]
            lux = get_luxwert(ap_id)
            return JsonResponse({"lux": lux})

    return JsonResponse({"lux": "kein Sensor angeschlossen"})





#Hier kommen die Funktionen f�r die An- und Abmeldung des Arbeitsplatzes

@never_cache
@login_required
def arbeitsplatz_buchen(request):
    if request.method == "POST":
        desk_id = request.POST.get("desk_id")
        start = request.POST.get("start_datetime")
        ende = request.POST.get("ende_datetime")

        try:
            startzeit = datetime.strptime(start, "%Y-%m-%dT%H:%M")
            endzeit = datetime.strptime(ende, "%Y-%m-%dT%H:%M")
        except ValueError:
            return HttpResponse("Ungültiges Datumsformat.") 
        
        if endzeit <= startzeit:
            return HttpResponse("Endzeit muss nach Startzeit liegen.")

        with open(arbeitsplaetze, "r") as datei:
            daten = json.load(datei)

        for arbeitsplatz in daten["arbeitsplaetze"]:
            if arbeitsplatz["id"] == desk_id and arbeitsplatz["status"] == "frei":
                arbeitsplatz["status"] = "belegt"
                arbeitsplatz["user_id"] = request.session.get("user_id")
                arbeitsplatz["startzeit"] = start
                arbeitsplatz["endzeit"] = ende

                if "luxsensor" in arbeitsplatz:
                    sensor_info = arbeitsplatz["luxsensor"]
                    start_sensor(arbeitsplatz["id"], sensor_info["i2c_bus"], sensor_info["i2c_address"])
                break


        with open(arbeitsplaetze, "w") as datei:
            json.dump(daten, datei, indent=4)

    return redirect("hauptseite")


@never_cache
@login_required
def arbeitsplatz_abmelden(request):
    user_id = request.session.get("user_id")

    with open(arbeitsplaetze, "r") as f:
        daten = json.load(f)

    desk_id = None
    startzeit = None
    endzeit = None

    for arbeitsplatz in daten["arbeitsplaetze"]:
        if arbeitsplatz["user_id"] == user_id and arbeitsplatz["status"] == "belegt":
            arbeitsplatz["status"] = "frei"
            arbeitsplatz["user_id"] = None
            desk_id = arbeitsplatz["id"]
            startzeit = arbeitsplatz.get("startzeit")
            endzeit = arbeitsplatz.get("endzeit")
            arbeitsplatz.pop("startzeit", None)
            arbeitsplatz.pop("endzeit", None)

            if "luxsensor" in arbeitsplatz:
                stop_sensor(arbeitsplatz["id"])
            break  

    if desk_id and startzeit and endzeit:
        try:
            start_dt = datetime.strptime(startzeit, "%Y-%m-%dT%H:%M")
            end_dt = datetime.strptime(endzeit, "%Y-%m-%dT%H:%M")
            dauer = int((end_dt - start_dt).total_seconds() / 60)
        except Exception:
            dauer = 0
            start_dt = None
            end_dt = None

        try:
            with open(rechnungsbelege, "r") as f:
                belege = json.load(f)
        except (FileNotFoundError, json.JSONDecodeError):
            belege = {"buchungen": []}

        if start_dt and end_dt:
            belege["buchungen"].append({
                "id": str(uuid.uuid4()),
                "benutzer": request.session.get("username"),
                "arbeitsplatz_id": desk_id,
                "startzeit": start_dt.strftime("%Y-%m-%d %H:%M"),
                "endzeit": end_dt.strftime("%Y-%m-%d %H:%M"),
                "dauer_minuten": dauer
            })

            with open(rechnungsbelege, "w") as f:
                json.dump(belege, f, indent=4)

    # Konvertiere datetime-Objekte in allen Arbeitsplätzen zu Strings
    for arbeitsplatz in daten["arbeitsplaetze"]:
        if type(arbeitsplatz.get("startzeit")) == datetime:
            arbeitsplatz["startzeit"] = arbeitsplatz["startzeit"].strftime("%Y-%m-%dT%H:%M")
        if type(arbeitsplatz.get("endzeit")) == datetime:
            arbeitsplatz["endzeit"] = arbeitsplatz["endzeit"].strftime("%Y-%m-%dT%H:%M")

    with open(arbeitsplaetze, "w") as f:
        json.dump(daten, f, indent=4)

    return redirect("hauptseite")


# Funktionen in den Profil-Einstelungen
 
# Funktion für die Ablegung der Rechnungen im Profil

@login_required
def buchungsuebersicht(request):
    username = request.session.get("username")
    buchungen = []

    try:
        with open(rechnungsbelege, "r") as file:
            daten = json.load(file)
            for buchung in daten["buchungen"]:
                if buchung["benutzer"] == username:
                    buchungen.append(buchung)
    except FileNotFoundError:
        pass

    return render(request, "iot_projekt/buchungsuebersicht.html", {"buchungen": buchungen})

# Funktion als CSV-Download

@never_cache
@login_required
def download_als_csv(request):
    import csv
    from django.http import HttpResponse

    buchung_id = request.GET.get("buchung_id")
    username = request.session.get("username")

    with open(rechnungsbelege, "r") as f:
        daten = json.load(f)

    # Nur die Buchungen des eingeloggten Benutzers
    user_buchungen = [
        b for b in daten.get("buchungen", [])
        if b.get("benutzer") == username
    ]

    if buchung_id:
        # Nur eine bestimmte Buchung exportieren
        buchung = next((b for b in user_buchungen if b.get("id") == buchung_id), None)
        if not buchung:
            return HttpResponse("Buchung nicht gefunden.", status=404)
        buchungen = [buchung]
        filename = f"buchung_{buchung_id}.csv"
    else:
        # Alle Buchungen des Users
        buchungen = user_buchungen
        filename = f"buchungen_{username}.csv"

    # CSV erzeugen
    response = HttpResponse(content_type="text/csv")
    response["Content-Disposition"] = f'attachment; filename="{filename}"'

    writer = csv.writer(response)
    writer.writerow(["Benutzer", "Startzeit", "Endzeit", "Arbeitsplatz", "Dauer (Minuten)"])
    for b in buchungen:
        writer.writerow([
            b.get("benutzer"),
            b.get("startzeit"),
            b.get("endzeit"),
            b.get("arbeitsplatz_id"),
            b.get("dauer_minuten", "")
        ])

    return response




# Funktion zum Passwort ändern

@login_required
def passwort_aendern(request):
    if request.method == "POST":
        pass1 = request.POST.get("passwort1")
        pass2 = request.POST.get("passwort2")

        if pass1 != pass2:
            messages.error(request, "Passwörter stimmen nicht überein.")
            return render(request, "iot_projekt/passwort_aendern.html")

        username = request.session.get("username")

        with open(registrierte_benutzer, "r") as file:
            daten = json.load(file)

        for user in daten["users"]:
            if user["username"] == username:
                user["password"] = make_password(pass1)
                break

        with open(registrierte_benutzer, "w") as file:
            json.dump(daten, file, indent=4)

        messages.success(request, "Passwort erfolgreich geändert.")
        return redirect("hauptseite")

    return render(request, "iot_projekt/passwort_aendern.html")



# Funktion zum Löschen des Profils

@login_required
def profil_loeschen(request):
    username = request.session.get("username")

    try:
        #Benutzer löschen
        with open(registrierte_benutzer, "r") as file:
            data = json.load(file)

        neue_liste = [user for user in data["users"] if user["username"] != username]
        data["users"] = neue_liste

        with open(registrierte_benutzer, "w") as file:
            json.dump(data, file, indent=4)

        #Buchungen löschen
        try:
            with open(rechnungsbelege, "r") as f:
                belege = json.load(f)
                neue_buchungen = [
                    buchung for buchung in belege.get("buchungen", [])
                    if buchung.get("benutzer") != username
                ]
                belege["buchungen"] = neue_buchungen

            with open(rechnungsbelege, "w") as f:
                json.dump(belege, f, indent=4)

        except (FileNotFoundError, json.JSONDecodeError):
            pass

    except Exception as e:
        return HttpResponse("Fehler beim Löschen des Profils: " + str(e))

    request.session.flush()
    return redirect("start")



