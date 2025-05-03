
import requests
import pytz
from datetime import datetime, timedelta
from geopy.geocoders import Nominatim
from geopy.exc import GeocoderUnavailable
from requests.exceptions import RequestException, ConnectionError
from urllib3.exceptions import MaxRetryError, NameResolutionError
import certifi
import ssl
import pycountry
from timezonefinder import TimezoneFinder
from io import BytesIO
from PIL import Image
from dotenv import load_dotenv
import os

class WeatherFetcher:
    def __init__(self):
        load_dotenv()
        self.API_KEY = os.getenv("OPENWEATHER_API_KEY")
        self.FLAG_URL = "https://flagsapi.com/{}/flat/64.png"
        
        # Set the SSL certificate path
        ssl_context = ssl.create_default_context(cafile=certifi.where())
        self.geolocator = Nominatim(user_agent="geoapiExercise", ssl_context=ssl_context)
        self.timezone_finder = TimezoneFinder()

    def get_location(self, city):
        # Get location data using geopy"""
        try:
            location = self.geolocator.geocode(city)
            if location is None:
                raise ValueError("City not found")
            return location
        except (GeocoderUnavailable, ConnectionError, MaxRetryError, NameResolutionError) as e:
            raise ConnectionError("Network error: Check your internet connection or servers might be down")
        except Exception as e:
            raise ValueError(f"Geocoding error: {str(e)}")

    def get_timezone_info(self, longitude, latitude):
        # Get timezone information for location"""
        timezone_str = self.timezone_finder.timezone_at(lng=longitude, lat=latitude)
        if timezone_str:
            time_zone = pytz.timezone(timezone_str)
            local_time = datetime.now(time_zone)
            return {
                'current_time': local_time.strftime("%I:%M %p"),
                'day': local_time.strftime("%A"),
                'date': local_time.strftime("%d %B %Y"),
                'timezone': time_zone
            }
        return None

    def fetch_weather_data(self, city):
        # Main method to fetch all weather data"""
        try:
            # Get location data first
            location = self.get_location(city)
            
            # Get timezone information
            timezone_info = self.get_timezone_info(location.longitude, location.latitude)
            if not timezone_info:
                timezone_info = {
                    'current_time': "Timezone not found",
                    'day': "N/A",
                    'date': "N/A",
                    'timezone': None
                }

            # Fetch current weather data
            api_url_current = f"https://api.openweathermap.org/data/2.5/weather?q={city}&appid={self.API_KEY}&units=metric"
            response_current = requests.get(api_url_current)
            response_current.raise_for_status()
            current_data = response_current.json()

            # Fetch forecast data
            api_url_forecast = f"https://api.openweathermap.org/data/2.5/forecast?q={city}&appid={self.API_KEY}&units=metric"
            response_forecast = requests.get(api_url_forecast)
            response_forecast.raise_for_status()
            forecast_data = response_forecast.json()

            # Get country info
            country_code = current_data["sys"]["country"]
            try:
                country = pycountry.countries.get(alpha_2=country_code).name
            except AttributeError:
                country = country_code

            # Get flag image
            flag_url = self.FLAG_URL.format(country_code)
            flag_response = requests.get(flag_url)
            flag_img = None
            if flag_response.status_code == 200:
                img_data = BytesIO(flag_response.content)
                flag_img = Image.open(img_data)
                flag_img = flag_img.resize((50, 48))

            # Prepare the weather data
            weather_data = {
                'location': location,
                'timezone_info': timezone_info,
                'current_data': current_data,
                'forecast_data': forecast_data,  # Fixed typo from 'forecast_data'
                'country': country,
                'country_code': country_code,
                'flag_img': flag_img,
                'city': city
            }

            return weather_data

        except RequestException as e:
            raise RequestException(f"API Request Failed: {str(e)}")
        except Exception as e:
            raise Exception(f"Error fetching weather data: {str(e)}")

    def is_daytime(self, sunrise, sunset, timezone_offset):
        # Determine if it's currently daytime"""
        sunrise_time = datetime.fromtimestamp(sunrise + timezone_offset, tz=pytz.utc)
        sunset_time = datetime.fromtimestamp(sunset + timezone_offset, tz=pytz.utc)
        current_time = datetime.now(pytz.utc) + timedelta(seconds=timezone_offset)
        return sunrise_time < current_time < sunset_time