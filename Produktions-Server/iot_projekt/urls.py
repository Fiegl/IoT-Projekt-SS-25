from django.urls import path
from . import views

urlpatterns = [
    path('', views.start, name='start'),
    path('logout/', views.logout_view, name='logout'),
    path('registrieren/', views.registrieren, name='registrieren'),
    path('mainpage/', views.hauptseite, name='hauptseite'),
    path('passwort_vergessen/', views.passwort_vergessen, name='passwort_vergessen'),
    path('passwort_zuruecksetzen/<str:token>/', views.passwort_zuruecksetzen, name='passwort_zuruecksetzen'),
]
