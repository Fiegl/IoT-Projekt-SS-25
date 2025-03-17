from django.shortcuts import render, redirect
from django.views import View
from django.http import HttpResponse


#Pfade zu den JSON-Dateien

registrierte_benutzer = "/var/www/django-project/datenbank/users.json" 


def home(request):
    return HttpResponse("Willkommen auf der Startseite!")
