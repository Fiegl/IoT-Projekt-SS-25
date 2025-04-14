from django.urls import path
from . import views
from .views import logout_view

urlpatterns = [
    path('', views.start, name='start'),
    path('registrieren/', views.registrieren, name='registrieren'),
    path('mainpage/', views.hauptseite, name='hauptseite'),
    path('logout/', logout_view, name='logout')
]
