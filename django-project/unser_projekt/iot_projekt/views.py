from django.shortcuts import render

def login_view(request):
    return render(request, 'iot_projekt/login.html')

def register_view(request):
    return render(request, 'iot_projekt/register.html')



