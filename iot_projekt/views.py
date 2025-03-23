from django.shortcuts import render, redirect
from django.views import View
from django.http import HttpResponse


#Pfade zu den JSON-Dateien

registrierte_benutzer = "/var/www/django-project/datenbank/users.json" 

def start(request):
    return render(request, 'start.html')

def registrieren(request):
    return render(request, 'registrieren.html')

def hauptseite(request):
    return render(request, 'mainpage.html')
