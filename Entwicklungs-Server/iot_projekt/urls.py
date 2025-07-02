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
    path('buchungsuebersicht', views.buchungsuebersicht, name='buchungsuebersicht'),
    path('passwort_aendern', views.passwort_aendern, name='passwort_aendern'),
    path("profil_loeschen/", views.profil_loeschen, name="profil_loeschen"),
    path('download_als_csv/', views.download_als_csv, name='download_als_csv'),
    path("luxwert/", views.luxwert_aktuell, name="luxwert"),
    path("sprache/<str:sprache>/", views.sprache_wechseln, name="sprache_wechseln"),
    path('api/status/', views.get_status_for_raspi, name='status_api'),
]


