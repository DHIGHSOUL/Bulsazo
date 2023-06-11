import requests
import json

api_key = 'f818dc3ab46f71e4bf9baec863c71948'
lat = 36.7720594357264
lon = 126.93186457301353

openWeather = f'http://api.openweathermap.org/data/2.5/forecast?lat={lat}&lon={lon}&appid={api_key}'

response = requests.get(openWeather)
jsonResponse = json.loads(response.text)

for item in jsonResponse['list']:
    date_time = item['dt_txt']
    temperatureKelvin = item['main']['temp']
    temperature = temperatureKelvin - 273.15
    weather_main = item['weather'][0]['main']
    rain3h = item['rain']['3h'] if 'rain' in item else 0

    print(f'Date and Time: {date_time}')
    print(f'Temperature: {temperature:.01f}°C')
    print(f'Weather code: {weather_main}')
    print(f'Rainfall for the last 3 hours: {rain3h}mm\n')