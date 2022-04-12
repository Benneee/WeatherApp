from flask import render_template, redirect, url_for
import requests
from app import app


@app.route('/')
@app.route('/index')
def index():
    title = "Weather App"
    city = 'Lagos'
    weather_data_list = []
    url = f'https://api.openweathermap.org/data/2.5/weather?q={city}&appid=0c221817ce583131b5d1bda6fbda6205'
    weather = requests.get(url).json()

    weather_data = {
        'icon': weather['weather'][0]['icon'],
        'description': weather['weather'][0]['description'],
        'temp': round((weather['main']['temp'] - 273), 2),
        'location': weather['name']+', '+weather['sys']['country'],
        'feels_like': round((weather['main']['feels_like'] - 273), 2),
        'humidity': weather['main']['humidity'],
        'wind': weather['wind']['speed']
    }
    weather_data_list.append(weather_data)
    return render_template('index.html', title=title, weather_data=weather_data_list)