from django.shortcuts import render

def login_iot_view(request):
    return render(request, 'iot_projekt/login_iot.html')

def register_iot_view(request):
    return render(request, 'iot_projekt/register_iot.html')



