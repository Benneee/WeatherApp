from flask import redirect, render_template, url_for, request, flash
from app import app, db
from app.helpers import get_weather_data
from app.models import City

@app.route('/', methods=['GET'])
def index():
    title = "Weather App"
    weather_data_list = []
    cities = City.query.all()

    for city in cities:
        weather = get_weather_data(city.name)

        weather_data = {
            'icon': weather['weather'][0]['icon'],
            'description': weather['weather'][0]['description'],
            'temp': round((weather['main']['temp'] - 273), 2),
            'location': weather['name']+', '+weather['sys']['country'],
            'feels_like': round((weather['main']['feels_like'] - 273), 2),
            'humidity': weather['main']['humidity'],
            'wind': weather['wind']['speed'],
            'city': weather['name']
        }
        weather_data_list.append(weather_data)

    return render_template('index.html', title=title, weather_data=reversed(weather_data_list))


@app.route('/', methods=['POST'])
def add_new_weather_data():
    city_to_add = request.form.get('city')

    if city_to_add:
        # First, we check if the city was already in the DB
        city = City.query.filter_by(name=city_to_add).first()
        
        if not city:
            # Now check if city is an actual city
            weather = get_weather_data(city_to_add)
            if weather['cod'] == 200:
                # add city to DB
                new_city = City(name=city_to_add)
                db.session.add(new_city)
                db.session.commit()
                flash('City added successfully!', category="success")
            else:
                flash('City entered is not a real city in the world!', category="danger")
        else:
            # city already exists in the DB, so we don't add it
            flash('City already exists!', category="danger")

    return redirect(url_for('index'))


@app.route('/city/<string:name>')
def delete_weather_data(name):
    city = City.query.filter_by(name=name).first()
    db.session.delete(city)
    db.session.commit()
    flash('City deleted successfully!', category="success")
    return redirect(url_for('index'))
