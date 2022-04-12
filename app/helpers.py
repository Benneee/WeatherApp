import requests


def get_weather_data(city):
    url = f'https://api.openweathermap.org/data/2.5/weather?q={city}&appid=0c221817ce583131b5d1bda6fbda6205'
    weather = requests.get(url).json()
    return weather;