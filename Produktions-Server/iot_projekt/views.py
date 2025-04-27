import json
import uuid
from django.shortcuts import render, redirect
from django.http import JsonResponse
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt
from django.views import View
from django.contrib.auth.hashers import make_password, check_password
from django.contrib.auth import logout
from django.core.mail import send_mail #wird für Passwort zurücksetzen benötigt
from functools import wraps #wird für den Decorator benötigt
from django.views.decorators.cache import never_cache #verhindert den Cache

# Pfad zu den JSON-Datenbanken

registrierte_benutzer = "/var/www/django-project/datenbank/users.json"
reset_tokens = "/var/www/django-project/datenbank/reset_tokens.json"
arbeitsplaetze = "/var/www/django-project/datenbank/arbeitsplaetze.json"


#Hier ist die Funktion für den Decorator
def login_required(view_func):
    @wraps(view_func)
    def wrapper(request, *args, **kwargs):
        if not request.session.get("username"):
            return redirect("start")
        return view_func(request, *args, **kwargs)
    return wrapper

#Hier sind die Funktionen für die Registrierung und das Ein- und Ausloggen

@never_cache
def registrieren(request):
    if request.method == "POST":
        username = request.POST.get("username")
        email = request.POST.get("email")
        password = request.POST.get("passwort")

        password_hash = make_password(password)


        with open(registrierte_benutzer, "r") as file:
            data = json.load(file)

        new_user = {
            "username": username,
            "email": email,
            "password": password_hash
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
                return redirect("hauptseite")
        return HttpResponse("Login fehlgeschlagen")
    
    return render(request, 'iot_projekt/start.html')

@never_cache
@login_required
def logout_view(request):
    logout(request)
    request.session.flush()
    return redirect("start")




#Hier sind die Funktionen für das Passwort zurücksetzen (SMTP GMAIL, siehe settings.py)


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
                    'Passwort zurücksetzen – Desk-Share-Lock',
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
        return HttpResponse("Ungültiger oder abgelaufener Link.")

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

        # Token löschen
        del tokens[token]
        save_reset_tokens(tokens)

        return HttpResponse("Passwort erfolgreich geändert!")

    return render(request, 'iot_projekt/passwort_zuruecksetzen.html', {"token": token})


#Hier die Funktion für die MainPage
@never_cache
@login_required
def hauptseite(request):
    if "username" not in request.session:
        return redirect("start")
    return render(request, 'iot_projekt/mainpage.html')


