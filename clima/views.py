import requests
from django.http import JsonResponse
from django.conf import settings


def obtener_clima(request):
    lat = request.GET.get('lat')
    lon = request.GET.get('lon')
    api_key = settings.OPENWEATHER_API_KEY

    url = f"https://api.openweathermap.org/data/2.5/weather?lat={lat}&lon={lon}&appid={api_key}&units=metric&lang=es"
    response = requests.get(url)
    data = response.json()

    clima = {
        'temp': data['main']['temp'],
        'descripcion': data['weather'][0]['description'],
        'icono': data['weather'][0]['icon']
    }
    return JsonResponse(clima)
