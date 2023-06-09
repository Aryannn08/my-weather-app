from flask import Flask, render_template, request
import requests
from dotenv import load_dotenv
import os


app = Flask(__name__)
load_dotenv('.env')

def get_weather(city):
    
    API_Key = os.getenv('API_KEY')
    url = f"http://api.openweathermap.org/data/2.5/weather?q={city}&units=metric&appid={API_Key}"
    response = requests.get(url)
    data = response.json()
    
    if response.status_code != 200 or 'message' in data:
        # Handle error when the city is not found or API request fails
        error_message = "City not found. Please enter a valid city name."
        return {"error": error_message}
    else:
        temperature =  int(data['main']['temp'])
        description = data['weather'][0]['description']
        humidity = data['main']['humidity']
        windSpeed = data['wind']['speed']
        weatherCode = data['weather'][0]['id']
        iconid = data['weather'][0]['icon']
        return {"temperature": temperature, "description": description, "humidity": humidity,"windSpeed" : windSpeed, "iconid": iconid}

@app.route('/', methods=['GET', 'POST'])
def index():
    show_heading = True
    if request.method == 'POST':
        city = (request.form['city']).upper()
        weather = get_weather(city)
        show_heading = False
        if 'error' in weather:
            # Display error message on the HTML page
            return render_template('index.html', error=weather['error'], show_heading=show_heading)
        else:
            return render_template('index.html', city=city, weather=weather, show_heading=show_heading)
    return render_template('index.html',show_heading=show_heading)

if __name__ == '__main__':
    app.run(debug=True)
