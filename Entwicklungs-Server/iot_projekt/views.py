import json
import uuid
from django.shortcuts import render, redirect
from django.http import JsonResponse
from django.http import HttpResponse
from django.views import View
from django.contrib.auth.hashers import make_password, check_password
from django.contrib.auth import logout

#Pfade zu den JSON-Dateien

registrierte_benutzer = "C:\\Users\\Besitzer\\django-project\\datenbank\\users.json"
arbeitsplaetze = "C:\\Users\\Besitzer\\django-project\\arbeitsplaetze.json"


def registrieren(request):
    if request.method == "POST":
        username = request.POST.get("username")
        email = request.POST.get("email")
        matrikelnummer = request.POST.get("matrikelnummer")
        password = request.POST.get("passwort")

        with open(registrierte_benutzer, "r") as file:
            data = json.load(file)

        if any(user["username"] == username for user in data["users"]):
            return HttpResponse("Benutzername bereits vergeben.")

        new_user = {
            "id": str(uuid.uuid4()),
            "username": username,
            "email": email,
            "matrikelnummer": matrikelnummer,
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
                return redirect("hauptseite")

        return HttpResponse("Login fehlgeschlagen")

    return render(request, 'iot_projekt/start.html')


def logout_view(request):
    logout(request)
    request.session.flush()
    return redirect("start")


def hauptseite(request):
    if "username" not in request.session:
        return redirect("start")
    return render(request, 'iot_projekt/mainpage.html')

