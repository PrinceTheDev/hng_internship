from django.http import JsonResponse
import requests

def temp(city):
    url = f"http://api.openweathermap.org/data/2.5/weather?q={city}&appid=8f389303a5b5c54f783c86973f85ed63&units=metric"
    response = requests.get(url)
    data = response.json()
    return data.get('main', {}).get('temp', 'Unknown')

def location(ip):
    url = f"https://ipinfo.io/{ip}/json?token=3b525b596c6d04"
    response = requests.get(url)
    data = response.json()
    return data.get('city', 'Unknown')

def hello(request):
    user_name = request.GET.get('user_name', 'Guest')
    user_ip = request.META.get('REMOTE_ADDR', 'Unknown')
    address = location(user_ip)
    temperature = temp(address)
    greet = f"Hello, {user_name}!, the temperature is {temperature} degrees Celsius in {address}"

    data = {
        "user_ip": user_ip,
        "address": address,
        "greet": greet
    }

    return JsonResponse(data)
