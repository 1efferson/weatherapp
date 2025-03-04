import customtkinter as ctk
from geopy.geocoders import Nominatim
from CTkMessagebox import CTkMessagebox
from timezonefinder import TimezoneFinder
from datetime import *
import requests
import pytz
import certifi
import ssl
from PIL import Image
import time

# Set dark theme
ctk.set_appearance_mode("dark")  # Options: "dark", "light", "system"
ctk.set_default_color_theme("blue")  # You can try other themes like "blue" or "green"

class WeatherApp(ctk.CTk):
    def __init__(self):
        super().__init__()
        self.geometry("1400x700")
        self.title("WEATHER FORECAST APPLICATION")

        # self.image = Image.open("images/background.png")  # Ensure the file is in the same directory or provide the full path
        # self.ctk_image = ctk.CTkImage(light_image=self.image, size=(1920, 1080))  # Resize if needed/

        # Create a label to display the image
        # self.image_label = ctk.CTkLabel(self, image=self.ctk_image, text="")  # Empty text to show only the image
        # self.image_label.pack(pady=20)  # Adjust position


        # Initialize UI components
        self.initialize_Graphical_Interface()

        
    def initialize_Graphical_Interface(self):
        # Creating a frame for the forecast for the days of the week
        self.frame1 = ctk.CTkFrame(self, fg_color="#fff", corner_radius=20)
        self.frame1.place(relwidth=0.8, relheight=0.25, relx=0.5, rely=1.0, anchor="s")

        # Adding 7 labels to self.frame1 using .place
        days = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"]
        x_positions = [30, 210, 390, 570, 750, 930, 1110]  # Custom x-coordinates for label placement
        for i, day in enumerate(days):
            self.label = ctk.CTkLabel(self.frame1, text=day, width=100, height=50, font=("Arial", 16, "bold"), text_color="white", fg_color="black")
            self.label.place(x=x_positions[i], y=10)  # Placing labels at the top of frame1

        # Current_Day=datetime.now()
        # .cinfigure(Current_Day.strftime("%A"))



        # Label for Big temperature value on the right 
        self.Big_Temp_number = ctk.CTkLabel(self, text="°C", font=("Arial", 68, "bold"), fg_color="#fff", text_color="black", corner_radius=20)
        self.Big_Temp_number.place(relwidth=0.24, relheight=0.3, relx=0.7, rely=0.2)

        # The 5 labels on the left of the app window
        self.time_label = ctk.CTkLabel(self, text="Time", width=100, height=20, font=("Arial", 27, "bold"), text_color="black", fg_color="#fff", corner_radius=20)
        self.time_label.place(relwidth=0.1, relheight=0.1, relx=0.1, rely=0.08)

        self.day_label = ctk.CTkLabel(self, text="Day", width=100, height=20, font=("Arial", 18, "bold"), text_color="black", fg_color="#fff", corner_radius=20)
        self.day_label.place(relwidth=0.1, relheight=0.06, relx=0.1, rely=0.2)

        self.date_label = ctk.CTkLabel(self, text="Date", width=100, height=20, font=("Arial", 18, "bold"), text_color="black", fg_color="#fff", corner_radius=20)
        self.date_label.place(relwidth=0.1, relheight=0.06, relx=0.1, rely=0.3)

        self.current_city = ctk.CTkLabel(self, text="City", width=100, height=20, font=("Arial", 30, "bold"), text_color="black", fg_color="#fff", corner_radius=20)
        self.current_city.place(relwidth=0.2, relheight=0.09, relx=0.72, rely=0.02)

        self.longitude_latitude_label = ctk.CTkLabel(self, text="Lon/Lat", width=100, height=20, font=("Arial", 18, "bold"), text_color="black", fg_color="#fff", corner_radius=20)
        self.longitude_latitude_label.place(relwidth=0.2, relheight=0.06, relx=0.72, rely=0.12)

        # Labels for other weather conditions on top of the frame1
        self.humidity_label = ctk.CTkLabel(self, text="Humidity", width=100, height=20, font=("Arial", 18, "bold"), text_color="black", fg_color="#fff", corner_radius=20)
        self.humidity_label.place(relwidth=0.15, relheight=0.1, relx=0.12, rely=0.6)

        self.pressure_label = ctk.CTkLabel(self, text="Pressure", width=100, height=20, font=("Arial", 18, "bold"), text_color="black", fg_color="#fff", bg_color="transparent",
                                           corner_radius=20)
        self.pressure_label.place(relwidth=0.15, relheight=0.1, relx=0.33, rely=0.6)

        self.windspeed_label = ctk.CTkLabel(self, text="Windspeed", width=100, height=20, font=("Arial", 18, "bold"), text_color="black", fg_color="#fff", corner_radius=20)
        self.windspeed_label.place(relwidth=0.15, relheight=0.1, relx=0.54, rely=0.6)

        self.cloud_description_label = ctk.CTkLabel(self, text="Cloud State", width=100, height=20, font=("Arial", 18, "bold"), text_color="black", fg_color="#fff", corner_radius=20)
        self.cloud_description_label.place(relwidth=0.15, relheight=0.1, relx=0.74, rely=0.6)


        # Creating a frame for the searchbar to put the two images inside of it
        self.searchbar_frame = ctk.CTkFrame(self, fg_color="white", corner_radius=20)
        self.searchbar_frame.place(relwidth=0.3, relheight=0.05, relx=0.3, rely=0.1)

        # Load images using CTkImage
        self.searchbar_cloud_image = ctk.CTkImage(light_image=Image.open("images/searchbar_cloud1.png"), size=(30, 30))
        self.searchbar_search_image = ctk.CTkImage(light_image=Image.open("images/search_icon.png"), size=(30, 30))

        # Left-side image
        self.left_label_in_searchbar = ctk.CTkLabel(self.searchbar_frame, image=self.searchbar_cloud_image, text="", fg_color="transparent")
        self.left_label_in_searchbar.pack(side="left", padx=5, pady=5)

        # Add an entry box to the search bar
        self.search_entry = ctk.CTkEntry(self.searchbar_frame, font=("Arial", 16), text_color="black", placeholder_text="Search City Here", placeholder_text_color="blue", fg_color="white", border_width=0)
        self.search_entry.pack(side="left", expand=True, fill="both", padx=5)
        self.search_entry.focus()  # Auto-focus on entry field

        # Search button with the Right-side search image
        self.search_button = ctk.CTkButton(self.searchbar_frame,image=self.searchbar_search_image,text="", fg_color="white",hover_color="lightgrey",width=20, height=20,command=self.getweather)
        self.search_button.pack(side="right", padx=5, pady=5)

    def getweather(self):
        city = self.search_entry.get()

        if not city:
            CTkMessagebox(title="Error", message="Please enter a city name.", icon="cancel",sound=True, bg_color="white",fg_color="lightblue", border_color="lightblue")
            return

        # Set the SSL certificate path
        ssl_context =ssl.create_default_context(cafile=certifi.where())

            # Initialize the geolocator with the SSL context
        geolocator = Nominatim(user_agent="geoapiExercise", ssl_context=ssl_context)
        location = geolocator.geocode(city)

        if location is None:
            CTkMessagebox(title="Error", message="City not found. Please enter a valid city name.", icon="cancel", sound=True, bg_color="white",fg_color="lightblue", border_color="lightblue")
            return

        obj = TimezoneFinder()
        result = obj.timezone_at(lng=location.longitude, lat=location.latitude)

          # Update labels
        self.current_city.configure(text=f"{result}")
        self.longitude_latitude_label.configure(text=f"Lon: {round(location.longitude, 2)}°E, Lat: {round(location.latitude, 2)}°N")

        # Set the time
        time_zone = pytz.timezone(result)
        local_time = datetime.now(time_zone)
        current_time = local_time.strftime("%I:%M %p")
        self.time_label.configure(text=f"{current_time}")

        # API Key 
        API_KEY = "139926ce2221e79cadaf3b146b99a320"

        # API URL 
        api_url = f"https://api.openweathermap.org/data/2.5/forecast?lat={location.latitude}&lon={location.longitude}&appid={API_KEY}&units=metric"

        # Fetch weather data
        try:
            response = requests.get(api_url)
            json_data = response.json()

            # Extracting weather forecast for the first time slot
            forecast = json_data["list"][0]
            
            temperature = forecast["main"]["temp"]
            humidity = forecast["main"]["humidity"]
            pressure = forecast["main"]["pressure"]
            windspeed = forecast["wind"]["speed"]
            cloud_description = forecast["weather"][0]["description"]

            # Displaying weather information
            f"Temperature: {temperature}°C\n"
            f"Humidity: {humidity}%\n"
            f"Pressure: {pressure} hPa\n"
            f"Wind Speed: {windspeed} m/s\n"
            f"Description: {cloud_description.capitalize()}"

            # **Updating Labels with Data**
            self.Big_Temp_number.configure(text=f"{temperature}°C")
            self.humidity_label.configure(text=f"Humidity: {humidity}%")
            self.pressure_label.configure(text=f"Pressure: {pressure} hPa")
            self.windspeed_label.configure(text=f"Wind Speed: {windspeed} m/s")
            self.cloud_description_label.configure(text=f"Description: {cloud_description.capitalize()}")

        except requests.exceptions.RequestException as e:
            CTkMessagebox(title="Error", message=f"API Request Failed: {e}", icon="cancel")

            


if __name__ == "__main__":
    app = WeatherApp()
    app.mainloop()