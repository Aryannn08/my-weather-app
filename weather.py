from flask import Flask, render_template, request
import requests
from dotenv import load_dotenv
import os

app = Flask(__name__)
load_dotenv('.env')  # Ensure .env file is loaded

def get_weather(city):
    # Use the correct environment variable name
    API_Key = os.getenv('OPENWEATHER_API_KEY')
    url = f"http://api.openweathermap.org/data/2.5/weather?q={city}&units=metric&appid={API_Key}"
    response = requests.get(url)
    data = response.json()

    # Check for errors in the response
    if response.status_code != 200 or 'message' in data:
        error_message = data.get('message', "City not found. Please enter a valid city name.")
        return {"error": error_message}
    else:
        # Extract necessary weather data
        temperature = int(data['main']['temp'])
        description = data['weather'][0]['description']
        humidity = data['main']['humidity']
        windSpeed = data['wind']['speed']
        iconid = data['weather'][0]['icon']
        return {
            "temperature": temperature,
            "description": description,
            "humidity": humidity,
            "windSpeed": windSpeed,
            "iconid": iconid
        }

@app.route('/', methods=['GET', 'POST'])
def index():
    show_heading = True
    error_message = None  # Initialize error message variable
    if request.method == 'POST':
        city = request.form['city'].strip()  # Remove extra spaces from city input
        if not city:
            error_message = "Please enter a city name."
            return render_template('index.html', error=error_message, show_heading=show_heading)
        
        weather = get_weather(city)
        show_heading = False

        if 'error' in weather:
            # If there's an error, display the error message
            return render_template('index.html', error=weather['error'], show_heading=show_heading)
        else:
            # If weather data is found, render the page with the weather info
            return render_template('index.html', city=city, weather=weather, show_heading=show_heading)

    return render_template('index.html', show_heading=show_heading, error=error_message)

if __name__ == '__main__':
    app.run(debug=True)
