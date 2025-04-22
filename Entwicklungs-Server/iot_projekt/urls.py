from django.urls import path
from . import views

urlpatterns = [
    path('', views.start, name='start'),
    path('registrieren/', views.registrieren, name='registrieren'),
    path('mainpage/', views.hauptseite, name='hauptseite'),
    path('logout/', views.logout_view, name='logout')
]
