import json
import uuid
from django.shortcuts import render, redirect
from django.http import JsonResponse, HttpResponse
from django.views import View
from django.contrib.auth.hashers import make_password, check_password
from django.contrib.auth import logout
from django.contrib.auth.decorators import login_required

# Pfade zu den JSON-Dateien
registrierte_benutzer = "C:\\Users\\Besitzer\\django-project\\datenbank\\users.json"
arbeitsplaetze = "C:\\Users\\Besitzer\\django-project\\datenbank\\arbeitsplaetze.json"

def registrieren(request):
    if request.method == "POST":
        username = request.POST.get("username")
        email = request.POST.get("email")
        password = request.POST.get("passwort")

        with open(registrierte_benutzer, "r") as file:
            data = json.load(file)

        if any(user["username"] == username for user in data["users"]):
            return HttpResponse("Benutzername bereits vergeben.")

        new_user = {
            "id": str(uuid.uuid4()),
            "username": username,
            "email": email,
            "password": make_password(password)
        }

        data["users"].append(new_user)

        with open(registrierte_benutzer, "w") as file:
            json.dump(data, file, indent=4)

        return redirect("start")

    return render(request, 'iot_projekt/registrieren.html')

def start(request):
    if request.method == "POST":
        username = request.POST.get("username")
        password = request.POST.get("passwort")

        with open(registrierte_benutzer, "r") as file:
            data = json.load(file)

        for user in data["users"]:
            if user["username"] == username and check_password(password, user["password"]):
                request.session["username"] = username
                request.session["user_id"] = user["id"]  # Wichtig, damit wir später den Benutzer in Buchung kennen
                return redirect("hauptseite")

        return HttpResponse("Login fehlgeschlagen")

    return render(request, 'iot_projekt/start.html')

def logout_view(request):
    logout(request)
    request.session.flush()
    return redirect("start")


def hauptseite(request):
    with open(arbeitsplaetze, "r") as file:
        arbeitsplaetze_data = json.load(file)["arbeitsplaetze"]

    return render(request, 'iot_projekt/mainpage.html', {"arbeitsplaetze": arbeitsplaetze_data})


def arbeitsplatz_buchen(request):
    if request.method == "POST":
        desk_id = request.POST.get("desk_id")

        # JSON öffnen und Daten laden
        with open(arbeitsplaetze, "r") as file:
            data = json.load(file)

        # Arbeitsplatz suchen
        desk = None
        for arbeitsplatz in data["arbeitsplaetze"]:
            if arbeitsplatz["id"] == desk_id:
                desk = arbeitsplatz
                break

        if desk is not None:
            # Arbeitsplatz existiert
            if desk["status"] == "frei":
                # Arbeitsplatz ist frei → Buchen erlaubt
                desk["status"] = "belegt"
                desk["user_id"] = request.session.get("user_id")

                # JSON speichern, nur wenn Änderung gemacht wurde!
                with open(arbeitsplaetze, "w") as file:
                    json.dump(data, file, indent=4)
        else:
            # Arbeitsplatz wurde nicht gefunden
            pass  # (könnte man später verbessern, z.B. Fehlermeldung anzeigen)

        return redirect("hauptseite")

    # Falls kein POST, auch auf Hauptseite weiterleiten
    return redirect("hauptseite")


