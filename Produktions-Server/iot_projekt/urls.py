from django.urls import path
from . import views

urlpatterns = [
    path('', views.start, name='start'),
    path('logout/', views.logout_view, name='logout'),
    path('registrieren/', views.registrieren, name='registrieren'),
    path('mainpage/', views.hauptseite, name='hauptseite'),
    path('passwort_vergessen/', views.passwort_vergessen, name='passwort_vergessen'),
    path('passwort_zuruecksetzen/<str:token>/', views.passwort_zuruecksetzen, name='passwort_zuruecksetzen'),
    path('arbeitsplatz_buchen/', views.arbeitsplatz_buchen, name='arbeitsplatz_buchen'),
    path('arbeitsplatz_abmelden/', views.arbeitsplatz_abmelden, name='arbeitsplatz_abmelden'),
]
