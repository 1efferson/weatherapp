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
import time

# Set dark theme
ctk.set_appearance_mode("light")  # Options: "dark", "light", "system"
ctk.set_default_color_theme("blue")  # You can try other themes like "blue" or "green"

class WeatherApp(ctk.CTk):
    def __init__(self):
        super().__init__()
        self.geometry("1920x1000")
        self.title("WEATHER FORECAST APPLICATION")

        # Create a standard Tkinter Canvas for the background image and weather texts.
        self.canvas = tk.Canvas(self, width=1920, height=1000, highlightthickness=0)
        self.canvas.place(x=0, y=0, relwidth=1, relheight=1)

        # Load and display the background image.
        self.bg_image = Image.open("images/background.png").resize((1920,1000))
        self.bg_photo = ImageTk.PhotoImage(self.bg_image)
        self.canvas.create_image(0, 0, image=self.bg_photo, anchor="nw")

        # Initialize canvas-drawn weather text items.
        self.initialize_background_text()

        # Initialize the rest of the UI components (frames, searchbar, etc.)
        self.initialize_Graphical_Interface()

    def initialize_background_text(self):
        # Create canvas text items 
        # Helper function to compute the center coordinates based on relative placement.
        def calculate_center_coordinates(relx, rely, relwidth, relheight):
            cx = relx * 1920 + (relwidth * 1920) / 2
            cy = rely * 1000 + (relheight * 1000) / 2
            return cx, cy

        
        big_temp_center = calculate_center_coordinates(0.7, 0.2, 0.24, 0.3)     
        
        time_center = calculate_center_coordinates(0.1, 0.08, 0.1, 0.1)       
       
        day_center = calculate_center_coordinates(0.1, 0.2, 0.1, 0.06)           
        
        date_center = calculate_center_coordinates(0.1, 0.3, 0.1, 0.06)          
        
        city_center = calculate_center_coordinates(0.72, 0.02, 0.2, 0.09)       
        
        lonlat_center = calculate_center_coordinates(0.72, 0.12, 0.2, 0.06)      
      
        humidity_center = calculate_center_coordinates(0.12, 0.6, 0.15, 0.1)     
       
        pressure_center = calculate_center_coordinates(0.33, 0.6, 0.15, 0.1)  
        
        windspeed_center = calculate_center_coordinates(0.54, 0.6, 0.15, 0.1)    
        
        cloud_description_center = calculate_center_coordinates(0.74, 0.6, 0.15, 0.1)      

        # Create canvas text items with default texts.
        self.big_temp_text_id = self.canvas.create_text(big_temp_center, text="°C",
                                                         font=("Arial", 70, "bold"), fill="black", anchor="center")
        self.time_text_id = self.canvas.create_text(time_center, text="Time",
                                                     font=("Arial", 50, "bold"), fill="black", anchor="center")
        self.day_text_id = self.canvas.create_text(day_center, text="Day",
                                                    font=("Arial", 20, "bold"), fill="black", anchor="center")
        self.date_text_id = self.canvas.create_text(date_center, text="Date",
                                                     font=("Arial", 20, "bold"), fill="black", anchor="center")
        self.city_text_id = self.canvas.create_text(city_center, text="City",
                                                     font=("Arial", 32, "bold"), fill="black", anchor="center")
        self.lonlat_text_id = self.canvas.create_text(lonlat_center, text="Lon/Lat",
                                                       font=("Arial", 20, "bold"), fill="black", anchor="center")
        self.humidity_text_id = self.canvas.create_text(humidity_center, text="Humidity",
                                                         font=("Arial", 20, "bold"), fill="black", anchor="center")
        self.pressure_text_id = self.canvas.create_text(pressure_center, text="Pressure",
                                                         font=("Arial", 20, "bold"), fill="black", anchor="center")
        self.windspeed_text_id = self.canvas.create_text(windspeed_center, text="Windspeed",
                                                          font=("Arial", 20, "bold"), fill="black", anchor="center")
        self.cloud_text_id = self.canvas.create_text(cloud_description_center, text="Cloud State",
                                                      font=("Arial", 20, "bold"), fill="black", anchor="center")

    def initialize_Graphical_Interface(self):
        # Creating a frame for the forecast for the days of the week 
        self.frame1 = ctk.CTkScrollableFrame(self, bg_color="lightblue", fg_color="#fff", corner_radius=30,orientation="horizontal")
        self.frame1.place(relwidth=0.84, relheight=0.25, relx=0.5, rely=1.0, anchor="s")
        


        # Creating a frame for the searchbar to put the two images inside of it.
        self.searchbar_frame = ctk.CTkFrame(self, bg_color="lightblue", fg_color="white", corner_radius=30)
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

    def getweather(self, event=None):
        city = self.search_entry.get()

        if not city:
            CTkMessagebox(title="Error", message="Please enter a city name.", icon="cancel", sound=True,
                          bg_color="white", fg_color="lightblue", border_color="lightblue")
            return

        # Set the SSL certificate path.
        ssl_context = ssl.create_default_context(cafile=certifi.where())

        # Initialize the geolocator with the SSL context.
        geolocator = Nominatim(user_agent="geoapiExercise", ssl_context=ssl_context)
        location = geolocator.geocode(city)

        if location is None:
            CTkMessagebox(title="Error", message="City not found. Please enter a valid city name.", icon="cancel",
                          sound=True, bg_color="white", fg_color="lightblue", border_color="lightblue")
            return

        timezone_finder = TimezoneFinder()
        result = timezone_finder.timezone_at(lng=location.longitude, lat=location.latitude)

        # Set the time using the fetched timezone.
        time_zone = pytz.timezone(result)
        local_time = datetime.now(time_zone)
        current_time = local_time.strftime("%I:%M %p")

        # API Key 
        API_KEY = "139926ce2221e79cadaf3b146b99a320"
         
        api_url_current = f"https://api.openweathermap.org/data/2.5/weather?lat={location.latitude}&lon={location.longitude}&appid={API_KEY}&units=metric"
        api_url_forecast = f"https://api.openweathermap.org/data/2.5/forecast?lat={location.latitude}&lon={location.longitude}&appid={API_KEY}&units=metric"
              
        try:
            response_current = requests.get(api_url_current)
            json_current_data = response_current.json()
           
            response_forecast = requests.get(api_url_forecast)
            json_forecast_data = response_forecast.json()

            # current_data = json_current_data["weather"]
            
            temperature =json_current_data["main"]["temp"]
            humidity = json_current_data["main"]["humidity"]
            pressure = json_current_data["main"]["pressure"]
            windspeed = json_current_data["wind"]["speed"]
            cloud_description = json_current_data["weather"][0]["description"]
            

            # # Update canvas text items with new weather data.
            self.canvas.itemconfig(self.big_temp_text_id, text=f"{temperature}°C")
            self.canvas.itemconfig(self.humidity_text_id, text=f"Humidity: {humidity}%")
            self.canvas.itemconfig(self.pressure_text_id, text=f"Pressure: {pressure} hPa")
            self.canvas.itemconfig(self.windspeed_text_id, text=f"Wind Speed: {windspeed} m/s")
            self.canvas.itemconfig(self.cloud_text_id, text=f"Description: {cloud_description.capitalize()}")


            for i in range(len(json_forecast_data["list"])):
                frame = ctk.CTkFrame(self.frame1)
                frame.pack(side="left", pady=10, padx=10, anchor="w")

                # Given date-time string
                date_str = json_forecast_data["list"][i]["dt_txt"]
                datetime_object = datetime.strptime(date_str, "%Y-%m-%d %H:%M:%S")
                formatted_date = datetime_object.strftime("%a %I:%M %p")
                tmp = json_forecast_data["list"][i]["main"]["temp"]


                lbl = ctk.CTkLabel(frame, text=formatted_date, width=120, height=50, font=("Arial", 16, "bold"), text_color="white", fg_color="black", corner_radius=20)
                lbl.pack(side="top", fill="x", padx=5, pady=5) # Placing labels at the top of frame1

                icon_code = json_forecast_data["list"][i]["weather"][0]["icon"]
                icon_path = f"icon/{icon_code}@2x.png"

                # Load image with PIL
                image = Image.open(icon_path)

                # Convert it to CTkImage
                icon_photo = ctk.CTkImage(light_image=image, size=(50, 50))
                daily_label = ctk.CTkLabel(frame, text="", image=icon_photo)
                daily_label.pack(side="left", pady=5)
                daily_label.image = icon_photo  # Keep a reference to prevent garbage collection.

                temperatures_in_frame1_lbl = ctk.CTkLabel(frame, text=f"{tmp}°C", width=110, height=50, font=("Arial", 16, "bold"))
                temperatures_in_frame1_lbl.pack(side="right", pady=5)  # Placing labels at the top of frame1

            

        except requests.exceptions.RequestException as e:
            CTkMessagebox(title="Error", message=f"API Request Failed: {e}", icon="cancel")
            return

        # Update canvas text items for location and time.
        self.canvas.itemconfig(self.city_text_id, text=f"{result}")
        self.canvas.itemconfig(self.lonlat_text_id, text=f"Lon: {round(location.longitude, 2)}°E, Lat: {round(location.latitude, 2)}°N")
        self.canvas.itemconfig(self.time_text_id, text=f"{current_time}")
        self.canvas.itemconfig(self.day_text_id, text=local_time.strftime("%A"))
        self.canvas.itemconfig(self.date_text_id, text=local_time.strftime("%d %B %Y"))

if __name__ == "__main__":
    app = WeatherApp()
    app.mainloop()
