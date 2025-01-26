from django.urls import path
from . import views

urlpatterns = [
    path('', views.login_iot_view, name='login_iot'),
    path('register_iot/', views.register_iot_view, name='register_iot'),
]
