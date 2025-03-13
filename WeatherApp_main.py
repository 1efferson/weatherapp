import tkinter as tk
import customtkinter as ctk
from geopy.geocoders import Nominatim
from CTkMessagebox import CTkMessagebox
from timezonefinder import TimezoneFinder
from datetime import datetime
import requests
import pytz
import certifi
import ssl
from PIL import Image, ImageTk
import threading
import math
import pycountry
from io import BytesIO
from datetime import datetime,timedelta,timezone
from geopy.exc import GeocoderUnavailable
from requests.exceptions import RequestException, ConnectionError
from urllib3.exceptions import MaxRetryError, NameResolutionError
from dotenv import load_dotenv
import os



# Set dark theme
ctk.set_appearance_mode("light")  # Options: "dark", "light", "system"
ctk.set_default_color_theme("blue")  # You can try other themes like "blue" or "green"


class WeatherApp(ctk.CTk):
    def __init__(self):
        super().__init__()
        self.geometry("1920x1000")
        self.title("WEATHER FORECAST APPLICATION")

        # Set minimum and maximum window size
        self.minsize(800, 600)
        self.maxsize(1500, 900)

# 
        # Canvas for background
        self.canvas = tk.Canvas(self, width=1920, height=1000, highlightthickness=0)
        self.canvas.place(x=0, y=0, relwidth=1, relheight=1)
# 
        # Load background images
        self.day_bg = ImageTk.PhotoImage(Image.open("images/day1.jpg").resize((1920, 1000)))
        self.night_bg = ImageTk.PhotoImage(Image.open("images/night7.jpg").resize((1920, 1000)))
        self.bg_photo = self.canvas.create_image(0, 0, anchor="nw", image=self.day_bg)

        # Initialize the rest of the UI components (frames, searchbar, etc.)
        self.initialize_Graphical_Interface()

        # Spinner variables
        self.spinner_dots = []
        self.spinner_angle = 0
        self.spinner_active = False

    def initialize_Graphical_Interface(self):
       # Creating a frame for the searchbar to put the two images inside of it.
        self.searchbar_frame = ctk.CTkFrame(self, fg_color="white",)
        self.searchbar_frame.place(relwidth=0.3, relheight=0.05, relx=0.35, rely=0.1)


            # Load images using CTkImage.
        self.searchbar_cloud_image = ctk.CTkImage(light_image=Image.open("images/searchbar_cloud1.png"), size=(30, 30))
        self.searchbar_search_image = ctk.CTkImage(light_image=Image.open("images/search_icon.png"), size=(30, 30))

            # Left-side image.
        self.left_label_in_searchbar = ctk.CTkLabel(self.searchbar_frame, image=self.searchbar_cloud_image, text="",
                                                        fg_color="transparent")
        self.left_label_in_searchbar.pack(side="left", padx=5, pady=5)

            # Add an entry box to the search bar.
        self.search_entry = ctk.CTkEntry(self.searchbar_frame, font=("Arial", 16), text_color="black",
                                            placeholder_text="Search City Here", placeholder_text_color="blue",
                                            fg_color="white", border_width=0)
        self.search_entry.pack(side="left", expand=True, fill="both", padx=5)
        self.search_entry.focus()  # Auto-focus on entry field

        # Bind the Enter key on the search entry to trigger the getweather method.
        self.search_entry.bind("<Return>", self.getweather)

        # Search button with the right-side search image.
        self.search_button = ctk.CTkButton(self.searchbar_frame, image=self.searchbar_search_image, text="",
                                            fg_color="white", hover_color="lightgrey", width=20, height=20,
                                            command=self.getweather)
        self.search_button.pack(side="right", padx=5, pady=5)



         # Helper function to compute the center coordinates based on relative placement.
        def calculate_center_coordinates(relx, rely, relwidth, relheight):
                cx = relx * 1500 + (relwidth * 1500) / 2
                cy = rely * 900 + (relheight * 900) / 2
                return cx, cy

        big_temp_center = calculate_center_coordinates(0.7, 0.2, 0.24, 0.3)

        flag_position_center = calculate_center_coordinates (0.72, 0.02, 0.2, 0.17)

        city_name_center= calculate_center_coordinates(0.72, 0.12, 0.2, 0.06)

        time_center = calculate_center_coordinates(0.1, 0.08, 0.1, 0.1)

        day_center = calculate_center_coordinates(0.1, 0.2, 0.1, 0.06)

        date_center = calculate_center_coordinates(0.1, 0.3, 0.1, 0.06)

        country_center = calculate_center_coordinates(0.72, 0.02, 0.2, 0.09)

        lonlat_center = calculate_center_coordinates(0.7, 0.2, 0.24, 0.1)

        humidity_center = calculate_center_coordinates(0.12, 0.6, 0.15, 0.1)

        pressure_center = calculate_center_coordinates(0.33, 0.6, 0.15, 0.1)

        windspeed_center = calculate_center_coordinates(0.54, 0.6, 0.15, 0.1)

        cloud_description_center = calculate_center_coordinates(0.74, 0.6, 0.15, 0.1)



            # Create canvas text items without default texts.
        self.big_temp_text_id = self.canvas.create_text(big_temp_center, text="",
                                                            font=("Arial", 70, "bold"), fill="black", anchor="center")
        
        self.city_name_id = self.canvas.create_text(city_name_center, text="",
                                                            font=("Arial", 20, "bold"), fill="black", anchor="center")

        self.country_id= self.canvas.create_text(country_center, text="",
                                                            font=("Arial", 20, "bold"), fill="black", anchor="center")

        self.time_text_id = self.canvas.create_text(time_center, text="",
                                                        font=("Arial", 50, "bold"), fill="black", anchor="center")
        self.day_text_id = self.canvas.create_text(day_center, text="",
                                                        font=("Arial", 20, "bold"), fill="black", anchor="center")
        self.date_text_id = self.canvas.create_text(date_center, text="",
                                                        font=("Arial", 20, "bold"), fill="black", anchor="center")
       
        self.lonlat_text_id = self.canvas.create_text(lonlat_center, text="",
                                                            font=("Arial", 20, "bold"), fill="black", anchor="center")
        self.humidity_text_id = self.canvas.create_text(humidity_center, text="",
                                                            font=("Arial", 20, "bold"), fill="black", anchor="center")
        self.pressure_text_id = self.canvas.create_text(pressure_center, text="",
                                                            font=("Arial", 20, "bold"), fill="black", anchor="center")
        self.windspeed_text_id = self.canvas.create_text(windspeed_center, text="",
                                                                font=("Arial", 20, "bold"), fill="black", anchor="center")
        self.cloud_text_id = self.canvas.create_text(cloud_description_center, text="",
                                                            font=("Arial", 20, "bold"), fill="black", anchor="center")
        self.flag_label = self.canvas.create_image(flag_position_center, anchor="center")  # Create the image placeholder

# 
    def is_daytime(self, sunrise, sunset, timezone_offset):
        # """Determine if it's currently daytime based on sunrise and sunset times."""
        sunrise_time = datetime.fromtimestamp(sunrise + timezone_offset, tz=timezone.utc)
        sunset_time = datetime.fromtimestamp(sunset + timezone_offset, tz=timezone.utc)
        current_time = datetime.now(timezone.utc) + timedelta(seconds=timezone_offset)
        return sunrise_time < current_time < sunset_time


    def update_background(self, is_day):
        # """Update the background image based on day or night."""
        new_bg = self.day_bg if is_day else self.night_bg
        self.canvas.itemconfig(self.bg_photo, image=new_bg)


    # changing text colour to white if background is black because city=night
    def toggle_mode(self, is_day):
        # Toggle the text colors based on whether it's day or night.
    
        if is_day:
            self.update_text_colors("black")  # Set text color to black for day mode
        else:
            self.update_text_colors("white")  # Set text color to white for night mode

    def update_text_colors(self, color):
        # Update the color of all text items on the canvas.
    
        for item in self.canvas.find_all():
            if self.canvas.type(item) == "text":
                self.canvas.itemconfig(item, fill=color)


    def getweather(self, event=None):
        city = self.search_entry.get()

        if not city:
            CTkMessagebox(title="Error", message="Please enter a city name.", icon="cancel", sound=True,
                          bg_color="white", fg_color="lightblue", border_color="lightblue")
            return

        # Start the spinner
        self.start_spinner()

        # Start the weather fetching process in a separate thread
        threading.Thread(target=self.fetch_weather_data, args=(city,), daemon=True).start()

    def fetch_weather_data(self, city):
        # Set the SSL certificate path.
        ssl_context = ssl.create_default_context(cafile=certifi.where())

        # Initialize the geolocator with the SSL context.
        geolocator = Nominatim(user_agent="geoapiExercise", ssl_context=ssl_context)



        try:
            # Attempt to fetch location data
            location = geolocator.geocode(city)
        except (GeocoderUnavailable, ConnectionError, MaxRetryError, NameResolutionError) as e:
            # Handle network-related errors
            CTkMessagebox(
                title="Error",
                message="No internet, check your network connection.",
                icon="cancel",
                sound=True,
                bg_color="white",
                fg_color="lightblue",
                border_color="lightblue"
            )
            self.stop_spinner()  # Stop the spinner
            return
        except Exception as e:
            # Handle other unexpected errors
            CTkMessagebox(
                title="Error",
                message=f"An unexpected error occurred: {e}",
                icon="cancel",
                sound=True,
                bg_color="white",
                fg_color="lightblue",
                border_color="lightblue"
            )
            self.stop_spinner()  # Stop the spinner
            return

        if location is None:
            CTkMessagebox(
                title="Error",
                message="City not found. Please enter a valid city name.",
                icon="cancel",
                sound=True,
                bg_color="white",
                fg_color="lightblue",
                border_color="lightblue"
            )
            self.stop_spinner()  # Stop the spinner if city is not found
            return


        timezone_finder = TimezoneFinder()
        result = timezone_finder.timezone_at(lng=location.longitude, lat=location.latitude)

        # Set the time using the fetched timezone.
        if result:
                time_zone = pytz.timezone(result)
                local_time = datetime.now(time_zone)
                current_time = local_time.strftime("%I:%M %p")
        else:
            current_time = "Timezone not found"

        # API Key
        load_dotenv()  # Load environment variables from .env file
        API_KEY = os.getenv("OPENWEATHER_API_KEY")


        api_url_current = f"https://api.openweathermap.org/data/2.5/weather?q={city}&appid={API_KEY}&units=metric"
        api_url_forecast = f"https://api.openweathermap.org/data/2.5/forecast?q={city}&appid={API_KEY}&units=metric"
        FLAG_URL = "https://flagsapi.com/{}/flat/64.png"
        

        try:
            # Attempt to fetch weather data
            response_current = requests.get(api_url_current)
            response_current.raise_for_status()  # Raise an exception for HTTP errors
            json_current_data = response_current.json()

            country_code= json_current_data["sys"]["country"]
            country= pycountry.countries.get(alpha_2=country_code).name
                

            flag_url = FLAG_URL.format(country_code)
            flag_response = requests.get(flag_url)
            if flag_response.status_code == 200:
                img_data = BytesIO(flag_response.content)
                img = Image.open(img_data)
                img = img.resize((50, 48))

                # Resize flag
                self.flag_img = ImageTk.PhotoImage(img)
                self.canvas.itemconfig(self.flag_label, image=self.flag_img)
            else:
                self.flag_label.config(image="")


            response_forecast = requests.get(api_url_forecast)
            response_forecast.raise_for_status()  # Raise an exception for HTTP errors
            json_forecast_data = response_forecast.json()

            # Update weather data
            temperature = json_current_data["main"]["temp"]
            humidity = json_current_data["main"]["humidity"]
            pressure = json_current_data["main"]["pressure"]
            windspeed = json_current_data["wind"]["speed"]
            cloud_description = json_current_data["weather"][0]["description"]
            country=country

            # Update canvas text items with new weather data.

            self.canvas.itemconfig(self.big_temp_text_id, text=f"{temperature}°C")
            self.canvas.itemconfig(self.humidity_text_id, text=f"Humidity:\n{humidity}%")
            self.canvas.itemconfig(self.pressure_text_id, text=f"Pressure:\n{pressure} hPa")
            self.canvas.itemconfig(self.windspeed_text_id, text=f"Windspeed:\n{windspeed} m/s")
            self.canvas.itemconfig(self.cloud_text_id, text=f"Clouds:\n{cloud_description.capitalize()}")

                        # Load the images for the four weather parameters siting on frame 1
            self.pressure_icon = ImageTk.PhotoImage(Image.open("images/pressure1.png"))
            self.humidity_icon = ImageTk.PhotoImage(Image.open("images/humidity1.png"))
            self.wind_icon = ImageTk.PhotoImage(Image.open("images/windspeed1.png"))
            self.description_icon = ImageTk.PhotoImage(Image.open("images/cloud_description1.png"))

            # Create the image on canvas with specified coordinates (x, y)
            self.pressure_img_id = self.canvas.create_image(480, 585,anchor="w", image=self.pressure_icon)
            self.humidity_img_id = self.canvas.create_image(160,585, anchor="w", image=self.humidity_icon)
            self.wind_img_id = self.canvas.create_image(750, 585, anchor="w", image=self.wind_icon)
            self.description_img_id = self.canvas.create_image(1070, 585, anchor="w", image=self.description_icon)



            # Update forecast data
            self.frame1 = ctk.CTkScrollableFrame(self, fg_color="#fff",
                                                orientation="horizontal")
            self.frame1.place(relwidth=0.84, relheight=0.25, relx=0.5, rely=1.0, anchor="s")

            for i in range(7):
                frame = ctk.CTkFrame(self.frame1, fg_color="lightblue")
                frame.pack(side="left", pady=10, padx=10, anchor="w")

                # Given date-time string
                date_str = json_forecast_data["list"][i]["dt_txt"]
                datetime_object = datetime.strptime(date_str, "%Y-%m-%d %H:%M:%S")
                formatted_date = datetime_object.strftime("%a %I:%M %p")
                tmp = json_forecast_data["list"][i]["main"]["temp"]

                lbl = ctk.CTkLabel(frame, text=formatted_date, width=120, height=50, font=("Arial", 16, "bold"),
                                text_color="white", fg_color="black", corner_radius=20)
                lbl.pack(side="top", fill="x", padx=5, pady=5)  # Placing labels at the top of frame1

                icon_code = json_forecast_data["list"][i]["weather"][0]["icon"]
                icon_path = f"icon/{icon_code}@2x.png"

                # Load image with PIL
                image = Image.open(icon_path)

                # Convert it to CTkImage
                icon_photo = ctk.CTkImage(light_image=image, size=(50, 50))
                daily_label = ctk.CTkLabel(frame, text="", image=icon_photo)
                daily_label.pack(side="left", pady=5)
                daily_label.image = icon_photo  # Keep a reference to prevent garbage collection.

                temperatures_in_frame1_lbl = ctk.CTkLabel(frame, text=f"{tmp}°C", width=110, height=50,
                                                        font=("Arial", 16, "bold"))
                temperatures_in_frame1_lbl.pack(side="right", pady=5)  # Placing labels at the top of frame1

        except RequestException as e:
            # Handle other API request errors
            CTkMessagebox(
                title="Error",
                message=f"API Request Failed: {e}",
                icon="cancel",
                sound=True,
                bg_color="white",
                fg_color="lightblue",
                border_color="lightblue"
            )
        finally:
            self.stop_spinner()  # Stop the spinner after fetching data or if an error occurs

            # Update canvas text(geopy) items for location and time.
            self.canvas.itemconfig(self.country_id, text=f"{country}")
            self.canvas.itemconfig(self.city_name_id, text=f"{city}".capitalize())

            self.canvas.itemconfig(self.lonlat_text_id, text=f"Lon: {round(location.longitude, 2)}°E, Lat: {round(location.latitude, 2)}°N")
            self.canvas.itemconfig(self.time_text_id, text=f"{current_time}")
            self.canvas.itemconfig(self.day_text_id, text=local_time.strftime("%A"))
            self.canvas.itemconfig(self.date_text_id, text=local_time.strftime("%d %B %Y"))

 # 
        try:
            sunrise = json_current_data["sys"]["sunrise"]
            sunset = json_current_data["sys"]["sunset"]
            timezone_offset = json_current_data["timezone"]

            is_day = self.is_daytime(sunrise, sunset, timezone_offset)
            self.update_background(is_day)  # Update the background image (day or night)
            self.toggle_mode(is_day)  # Update text colors based on day/night

        except requests.exceptions.RequestException as e:
            CTkMessagebox(title="Error", message=f"API Request Failed: {e}", icon="cancel", sound=True)

    def start_spinner(self):
        """Start the spinning dots animation."""
        self.spinner_active = True
        self.spinner_dots = []
        self.spinner_angle = 0

        # Define center and radius as instance variables
        self.center_x = 750  # 1500 / 2
        self.center_y = 300  # 900 / 2
        self.radius = 50  # Radius of the spinner circle


        dot_colors = [
        "red", "green", "blue", "orange",
        "purple", "red", "magenta", "yellow"]


        # Create 8 dots in a circular pattern
        for i in range(8):
            angle = math.radians(45 * i)  # Calculate the angle for each dot
            x = self.center_x + 30 * math.cos(angle)  # Calculate x position
            y = self.center_y + 30 * math.sin(angle)  # Calculate y position
            dot = self.canvas.create_oval(x - 5, y - 5, x + 5, y + 5, fill=dot_colors[i])
            self.spinner_dots.append(dot)

        # Start the animation
        self.animate_spinner()

    def animate_spinner(self):
        """Animate the spinning dots."""
        if not self.spinner_active:
            return

        # Increment the angle for rotation
        self.spinner_angle = (self.spinner_angle + 5) % 360  # Increase angle by 5 degrees

        # Update the position of each dot
        for i, dot in enumerate(self.spinner_dots):
            angle = math.radians(45 * i + self.spinner_angle)  # Calculate the new angle for the dot
            x = self.center_x + 30 * math.cos(angle)  # Calculate new x position
            y = self.center_y + 30 * math.sin(angle)  # Calculate new y position
            self.canvas.coords(dot, x - 5, y - 5, x + 5, y + 5)  # Update dot position

        # Repeat every 50ms
        self.after(50, self.animate_spinner)

    def stop_spinner(self):
        """Stop the spinning dots animation."""
        self.spinner_active = False
        for dot in self.spinner_dots:
            self.canvas.delete(dot)
        self.spinner_dots = []

        
if __name__ == "__main__":
    app = WeatherApp()
    app.mainloop()