import requests
from datetime import datetime, timedelta

def get_weather(api_key, city, start_time, end_time):
    base_url = "http://api.openweathermap.org/data/2.5/forecast"
    params = {"q": city, "appid": api_key, "units": "metric"}
    
    try:
        response = requests.get(base_url, params=params)
        response.raise_for_status()  # Raise an exception for HTTP errors (if any)
        data = response.json()
        
        forecast_list = data["list"]
        weather_forecast = {}
        for forecast in forecast_list:
            forecast_time = datetime.fromtimestamp(forecast["dt"])
            if start_time <= forecast_time < end_time:
                # Group forecast data by 6-hour intervals
                interval = (forecast_time - start_time) // timedelta(hours=6)
                if interval not in weather_forecast:
                    weather_forecast[interval] = []
                weather_forecast[interval].append({
                    "description": forecast["weather"][0]["description"],
                    "temperature": forecast["main"]["temp"],
                    "humidity": forecast["main"]["humidity"],
                    "wind_speed": forecast["wind"]["speed"]
                })
        
        return weather_forecast
    except requests.exceptions.RequestException as e:
        print("Error connecting to the weather API:", e)
        return None
    except KeyError as e:
        print("Error parsing API response:", e)
        return None

if __name__ == "__main__":
    api_key = "4e73563844726e1bd873940e8bd30870"  
    city_name = input("Enter the city name for weather forecast: ")
    
    current_time = datetime.now()
    start_time = current_time.replace(hour=0, minute=0, second=0, microsecond=0)
    end_time = start_time + timedelta(days=4)
    
    weather_data = get_weather(api_key, city_name, start_time, end_time)
    
    if weather_data:
        print("\nWeather Forecast for", city_name, "over the next 4 days (6-hour intervals):")
        for interval, forecasts in weather_data.items():
            interval_time = start_time + timedelta(hours=interval * 6)
            print("\nInterval starting at", interval_time.strftime("%Y-%m-%d %H:%M:%S"))
            for forecast in forecasts:
                print("Description:", forecast["description"])
                print("Temperature (°C):", forecast["temperature"])
                print("Humidity (%):", forecast["humidity"])
                print("Wind Speed (m/s):", forecast["wind_speed"])
                print("-" * 30)
    else:
        print("Unable to fetch weather forecast. Please check the city name and your API key.")
