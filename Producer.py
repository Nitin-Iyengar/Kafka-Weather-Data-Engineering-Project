import pandas as pd
from kafka import KafkaProducer
from json import dumps
import requests
import random
import time
import json


producer = KafkaProducer(bootstrap_servers=['34.121.184.86:9092'],
                         value_serializer=lambda x: dumps(x).encode('utf-8'))

cities = ['Mumbai', 'Chennai', 'Kolkata', 'Bengaluru', 'Delhi', 'Hyderabad', 'Cochin', 'Pune', 'Ahmedabad',
          'Amritsar', 'Bhopal', 'Bhubaneswar', 'Chandigarh', 'Faridabad', 'Ghaziabad', 'Jamshedpur', 'Jaipur',
          'Kochi', 'Lucknow', 'Nagpur', 'Patna', 'Raipur', 'Surat', 'Visakhapatnam', 'Agra', 'Ajmer', 'Kanpur', 'Mysuru', 'Srinagar']

file_path = r"D:\Service Accounts\weather_api_key.json"  # Use raw string or forward slashes

with open(file_path) as f:
    api_key_data = json.load(f)
    weather_api_key = api_key_data['weather_api_key']


def fetch_weather_data(city):
    api_url = f"http://api.weatherapi.com/v1/current.json?key={weather_api_key}&q={city}&aqi=yes"
    response = requests.get(api_url)

    if response.status_code == 200:
        data = response.json()
        formatted_data = {
            "city": data["location"]["name"],
            "region": data["location"]["region"],
            "country": data["location"]["country"],
            "lat": data["location"]["lat"],
            "lon": data["location"]["lon"],
            "tz_id": data["location"]["tz_id"],
            "localtime_epoch": data["location"]["localtime_epoch"],
            "localtime": data["location"]["localtime"],
            "last_updated_epoch": data["current"]["last_updated_epoch"],
            "last_updated": data["current"]["last_updated"],
            "temp_c": data["current"]["temp_c"],
            "temp_f": data["current"]["temp_f"],
            "wind_mph": data["current"]["wind_mph"],
            "wind_kph": data["current"]["wind_kph"],
            "wind_degree": data["current"]["wind_degree"],
            "wind_dir": data["current"]["wind_dir"],
            "humidity": data["current"]["humidity"],
            "cloud": data["current"]["cloud"],
            "co": data["current"]["air_quality"]["co"],
            "no2": data["current"]["air_quality"]["no2"],
            "o3": data["current"]["air_quality"]["o3"],
            "so2": data["current"]["air_quality"]["so2"],
            "pm2_5": data["current"]["air_quality"]["pm2_5"],
            "pm10": data["current"]["air_quality"]["pm10"],
            "US_epa_index": data["current"]["air_quality"]["us-epa-index"],
            "GB_defra_index": data["current"]["air_quality"]["gb-defra-index"]
        }
        return formatted_data
    else:
        print(f"Failed to fetch data for {city}")
        return None


# Iterate infinitely through the list of cities
city_iterator = iter(cities)
while True:
    try:
        # Get the next city from the iterator
        city = next(city_iterator)
    except StopIteration:
        # Restart the iterator if it reaches the end of the list
        city_iterator = iter(cities)
        city = next(city_iterator)

    # Fetch weather data for the current city
    weather_data = fetch_weather_data(city)

    if weather_data:
        producer.send('weather_data', value=weather_data)
        producer.flush()  # Ensure message is sent immediately
    else:
        print(f"No weather data for {city}")

    # Adjust the time interval before fetching data for the next city
    time.sleep(5)  # Adjust the time interval as needed
