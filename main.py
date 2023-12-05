import requests
import random
import time

cities = ['Mumbai', 'Chennai', 'Kolkata', 'Bengaluru', 'Delhi', 'Hyderabad', 'Cochin', 'Pune', 'Ahmedabad']


def fetch_weather_data(city):
    api_url = f"http://api.weatherapi.com/v1/current.json?key=36d6b6dfa90741efa0e193320232411&q={city}&aqi=yes"
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
            "us-epa-index": data["current"]["air_quality"]["us-epa-index"],
            "gb-defra-index": data["current"]["air_quality"]["gb-defra-index"]
        }
        return formatted_data
    else:
        print(f"Failed to fetch data for {city}")
        return None


while True:
    # Pick a random city
    random_city = random.choice(cities)

    # Fetch weather data for the random city
    weather_data = fetch_weather_data(random_city)

    # Print the weather data (or do something with it)
    if weather_data:
        print(weather_data)

    # Wait for some time before fetching data again (for continuous process)
    time.sleep(10)  # Adjust the time interval as needed
