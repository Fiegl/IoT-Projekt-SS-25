import json
import uuid
from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib.auth.hashers import make_password, check_password
from django.contrib.auth import logout
from django.views.decorators.cache import never_cache
from datetime import datetime

# Pfade zu JSON-Dateien
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
                request.session["user_id"] = user["id"]

                return redirect("hauptseite")

        return HttpResponse("Ihr Passwort oder Benutzername ist falsch, bitte erneut eingeben.")

    return render(request, 'iot_projekt/start.html')



def logout_view(request):
    logout(request)
    request.session.flush()
    return redirect("start")


def hauptseite(request):
    if "username" not in request.session:
        return redirect("start")

    with open(arbeitsplaetze, "r") as file:
        arbeitsplaetze_data = json.load(file)["arbeitsplaetze"]
        
    user_id = request.session.get("user_id")

    return render(request, 'iot_projekt/mainpage.html', {"arbeitsplaetze": arbeitsplaetze_data, "user_id": user_id})



def arbeitsplatz_buchen(request):
    if request.method == "POST":
        desk_id = request.POST.get("desk_id")
        start = request.POST.get("start_datetime")
        ende = request.POST.get("ende_datetime")

        try:
            start_dt = datetime.strptime(start, "%Y-%m-%dT%H:%M")
            ende_dt = datetime.strptime(ende, "%Y-%m-%dT%H:%M")
        except ValueError:
            messages.error(request, "Ungültiges Datumsformat.")
            return redirect("startseite") 
        
        if ende_dt <= start_dt:
            messages.error(request, "Endzeit muss nach der Startzeit liegen.")
            return redirect("startseite")

        with open(arbeitsplaetze, "r") as datei:
            daten = json.load(datei)

        
        desk = None #Als Schutz vor unbefugten POST-Request (Manipulation von Formularen)
        
        for arbeitsplatz in daten["arbeitsplaetze"]:
            if arbeitsplatz["id"] == desk_id:
                desk = arbeitsplatz
                break

        if desk is not None:
        
            if desk["status"] == "frei":
                desk["status"] = "belegt"
                desk["user_id"] = request.session.get("user_id")

                
                with open(arbeitsplaetze, "w") as datei:
                    json.dump(daten, datei, indent=4)

    return redirect("hauptseite")



def arbeitsplatz_abmelden(request):
    if "user_id" not in request.session:
        return redirect("start")

    user_id = request.session["user_id"]

    with open(arbeitsplaetze, "r") as datei:
        daten = json.load(datei)

    for arbeitsplatz in daten["arbeitsplaetze"]:
        if arbeitsplatz["user_id"] == user_id and arbeitsplatz["status"] == "belegt":
            arbeitsplatz["status"] = "frei"
            arbeitsplatz["user_id"] = None
            break  

    with open(arbeitsplaetze, "w") as datei:
        json.dump(daten, datei, indent=4)

    return redirect("hauptseite")

