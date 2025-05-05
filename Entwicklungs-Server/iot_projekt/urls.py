from django.urls import path
from . import views

urlpatterns = [
    path('', views.start, name='start'),
    path('registrieren/', views.registrieren, name='registrieren'),
    path('mainpage/', views.hauptseite, name='hauptseite'),
    path('logout/', views.logout_view, name='logout'),
    path('arbeitsplatz_buchen/', views.arbeitsplatz_buchen, name='arbeitsplatz_buchen'),
    path('arbeitsplatz_abmelden/', views.arbeitsplatz_abmelden, name='arbeitsplatz_abmelden'),
]


