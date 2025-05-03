import tkinter as tk
import customtkinter as ctk
from CTkMessagebox import CTkMessagebox
from datetime import datetime
import requests
from PIL import Image, ImageTk
import threading
import math
import pycountry
from datetime import datetime
from dotenv import load_dotenv
import os
import json
from tkintermapview import TkinterMapView
from history_manager import HistoryManager
from voice_recognition import VoiceRecognition
from weather_fetcher import WeatherFetcher


# Set dark theme
ctk.set_appearance_mode("light")  # Options: "dark", "light", "system"
ctk.set_default_color_theme("blue")  # You can try other themes like "blue" or "green"


class WeatherApp(ctk.CTk):
    def __init__(self):
        super().__init__()
        self.geometry("1500x900")
        self.title("WEATHER FORECAST APPLICATION")

        # Canvas for background
        self.canvas = tk.Canvas(self, width=1500, height=900, highlightthickness=0)
        self.canvas.place(x=0, y=0, relwidth=1, relheight=1)

        # API Key
        load_dotenv()  # Load environment variables from .env file
        self.API_KEY = os.getenv("OPENWEATHER_API_KEY")

        # Initialize cities data
        self.cities_list = []  # Initialize empty list
        self.load_cities_data()  # Load cities data
        self.voice_recognizer = None

        self.history_manager = HistoryManager(self)
        self.voice_recognizer = VoiceRecognition(self.voice_callback)

        # Load background images
        self.day_bg = ImageTk.PhotoImage(Image.open("assets/images/day3.jpg").resize((1920, 1000)))
        self.night_bg = ImageTk.PhotoImage(Image.open("assets/images/night7.jpg").resize((1920, 1000)))
        self.rain_bg = ImageTk.PhotoImage(Image.open("assets/images/rain.jpg").resize((1920, 1000)))
        self.bg_photo = self.canvas.create_image(0, 0, anchor="nw", image=self.day_bg)

        # Initialize the rest of the UI components (frames, searchbar, etc.)
        self.initialize_Graphical_Interface()
       
        # map variables
        self.map_visible = False
        self.initialize_weather_map()
        self.map_frame.place_forget()


        # Spinner variables
        self.spinner_dots = []
        self.spinner_angle = 0
        self.spinner_active = False


    def load_cities_data(self):
        # Load cities data from JSON file
        try:
            with open("cities.json", "r", encoding="utf-8") as file:
                self.cities_list = json.load(file)
            print(f"Successfully loaded {len(self.cities_list)} cities")
        except Exception as e:
            print(f"Unexpected error loading cities")

    def initialize_Graphical_Interface(self):
       # Creating a frame for the searchbar to put the two images inside of it.
        self.searchbar_frame = ctk.CTkFrame(self, fg_color="white",)
        self.searchbar_frame.place(relwidth=0.3, relheight=0.05, relx=0.35, rely=0.1)


            # Load images using CTkImage.
        self.searchbar_cloud_image = ctk.CTkImage(light_image=Image.open("assets/images/searchbar_cloud1.png"), size=(30, 30))
        self.searchbar_search_image = ctk.CTkImage(light_image=Image.open("assets/images/search_icon.png"), size=(30, 30))
        self.history_image = ctk.CTkImage(light_image=Image.open("assets/images/history_image2.png"), size=(30, 30))

            # Left-side image.
        self.left_label_in_searchbar = ctk.CTkLabel(self.searchbar_frame, image=self.searchbar_cloud_image, text="",
                                                        fg_color="transparent")
        self.left_label_in_searchbar.pack(side="left", padx=5, pady=5)

            # entry box to the search bar.
        self.search_entry = ctk.CTkEntry(self.searchbar_frame, 
                                       font=("Arial", 16), 
                                       text_color="black",
                                       placeholder_text="Search City Here",
                                       placeholder_text_color="blue",
                                       fg_color="white", 
                                       border_width=0)
        self.search_entry.pack(side="left", expand=True, fill="both", padx=5)
        self.search_entry.bind("<KeyRelease>", self.update_suggestions)
        self.search_entry.focus()

        # Create suggestion dropdown
        self.suggestion_menu = ctk.CTkOptionMenu(
            self.searchbar_frame,
            values=[],
            fg_color="white",
            text_color="black",
            button_color="white",
            button_hover_color="lightgray",
            anchor="w",
            command=self.select_city
        )
        self.suggestion_menu.pack(side="left", fill="x", expand=True)
        self.suggestion_menu.set("")
        self.suggestion_menu.pack_forget()

        self.voice_button = ctk.CTkButton(self, text="🎤", command=self.handle_voice_input, width = 50, height = 45, fg_color="transparent", hover_color="lightgrey")
        self.voice_button.place(relx=0.66, rely=0.10)
        
        self.voice_output_text_id = self.canvas.create_text( 750, 70, text="", font=("Arial", 14), fill="black", anchor="center")


        # Bind the Enter key on the search entry to trigger the getweather method.
        self.search_entry.bind("<Return>", self.getweather)

        # Bind key release event for suggestions
        self.search_entry.bind("<KeyRelease>", self.update_suggestions)
    
        # Search button with the right-side search image.
        self.search_button = ctk.CTkButton(self.searchbar_frame, image=self.searchbar_search_image, text="",
                                            fg_color="white", hover_color="lightgrey", width=20, height=20,
                                            command=self.getweather)
        self.search_button.pack(side="right", padx=5, pady=5)

        search_history_button = ctk.CTkButton(self,image=self.history_image,text="",fg_color="transparent",hover_color="lightgrey", width=50,height=45,command=self.history_manager.show_history)
        search_history_button.place(relx=0.94, rely=0.05) 


        # Add map toggle button
        self.map_button = ctk.CTkButton(self, text="🌍 Show Map", text_color="black", command=self.toggle_map, width=100, height=40,fg_color="transparent",hover_color="lightgrey")
        self.map_button.place(relx=0.01, rely=0.04)  

        # Create canvas text items
        self.big_temp_text_id = self.canvas.create_text(1275, 315, text="",font=("Arial", 70, "bold"), fill="black", anchor="center")

        self.city_name_id = self.canvas.create_text(1230, 135, text="",font=("Arial", 20, "bold"), fill="black", anchor="center")

        self.country_id = self.canvas.create_text(1230, 60, text="",font=("Arial", 20, "bold"), fill="black", anchor="center")

        self.time_text_id = self.canvas.create_text(225, 108, text="",font=("Arial", 50, "bold"), fill="black", anchor="center")

        self.day_text_id = self.canvas.create_text(180, 189, text="",font=("Arial", 20, "bold"), fill="black", anchor="center")

        self.date_text_id = self.canvas.create_text(180, 216, text="",font=("Arial", 20, "bold"), fill="black", anchor="center")

        self.lonlat_text_id = self.canvas.create_text(1260, 211, text="",font=("Arial", 20, "bold"), fill="black", anchor="center")

        self.humidity_text_id = self.canvas.create_text(292, 585, text="",font=("Arial", 20, "bold"), fill="black", anchor="center")

        self.pressure_text_id = self.canvas.create_text(607, 585, text="",font=("Arial", 20, "bold"), fill="black", anchor="center")

        self.windspeed_text_id = self.canvas.create_text(922, 585, text="",font=("Arial", 20, "bold"), fill="black", anchor="center")

        self.cloud_text_id = self.canvas.create_text(1237, 585, text="",font=("Arial", 20, "bold"), fill="black", anchor="center")

        self.flag_label = self.canvas.create_image(1230, 94, anchor="center")

        self.feels_like_text_id = self.canvas.create_text( 1275, 380, text="", font=("Arial", 24, "italic"), fill="black", anchor="center")

    def voice_callback(self, message: str):
        """Handle voice recognition status updates"""
        self.canvas.itemconfig(self.voice_output_text_id, text=message)
        self.update()  # Force UI update

    def handle_voice_input(self):
        """Handle voice button click"""
        if not self.voice_recognizer.is_listening:
            self.canvas.itemconfig(self.voice_output_text_id, text="Starting voice recognition...")
            recognized_text = self.voice_recognizer.listen()
            
            if recognized_text:
                self.search_entry.delete(0, "end")
                self.search_entry.insert(0, recognized_text)
                self.getweather()
        else:
            self.voice_recognizer.stop_listening()
            self.canvas.itemconfig(self.voice_output_text_id, text="Voice recognition stopped")

    # the update_suggestions method for the options/suggestions menu
    def update_suggestions(self, event):
        current_text = self.search_entry.get().strip()

        if len(current_text) < 1:
            self.suggestion_menu.pack_forget()
            return

        matching_cities = [
            city for city in self.cities_list 
            if city.get("name", "").capitalize().startswith(current_text.capitalize())
        ]

        values = []
        for city in matching_cities:
            country_code = city.get("country", "")
            flag_emoji = self.get_flag_emoji(country_code)
            try:
                country = pycountry.countries.get(alpha_2=country_code)
                country_name = country.name
            except AttributeError:
                country_name = country_code
            display_text = f"{flag_emoji} {city['name']}, {country_name}"
            values.append(display_text)

        if values:
            self.suggestion_menu.configure(values=values)
            self.suggestion_menu.pack(side="left", fill="x", expand=True)
        else:
            self.suggestion_menu.pack_forget()

    # method to convert country code to flag emoji
    def get_flag_emoji(self, country_code):
        if len(country_code) != 2:
            return ""
        code = country_code.upper()
        if not (code[0].isalpha() and code[1].isalpha()):
            return ""
        first = 0x1F1E6 + (ord(code[0]) - ord('A'))
        second = 0x1F1E6 + (ord(code[1]) - ord('A'))
        return chr(first) + chr(second)

    # Update the select_city method
    def select_city(self, choice):
        try:
            # Split into parts and extract city name
            parts = choice.split(', ', 1)
            left_part = parts[0]
            city_name = ' '.join(left_part.split(' ')[1:]).strip()
        except:
            city_name = choice.split(",")[0].strip()
        
        self.search_entry.delete(0, "end")
        self.search_entry.insert(0, city_name)
        self.suggestion_menu.pack_forget()
        self.getweather()
    
    def describe_feels_like(self, feels_like):
        if feels_like <= 0:
            return "Brutally cold."
        elif feels_like <= 10:
            return "Very cold"
        elif feels_like<= 16:
            return "Chilly"
        elif feels_like <= 21:
            return "Cool"
        elif feels_like <= 27:
            return "Comfortably warm"
        elif feels_like<= 32:
            return "Warm"
        elif feels_like<= 38:
            return "Getting COOKED"
        else:
            return "Scorching"


    def update_background(self, is_day, is_rain):
        # Update the background image based on day, night, or rain.
        if is_rain:
            new_bg = self.rain_bg
        else:
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
        try:
            # Initialize weather fetcher
            weather_fetcher = WeatherFetcher()
            
            # Fetch all weather data
            weather_data = weather_fetcher.fetch_weather_data(city)
            
            # Extract data from the response
            location = weather_data['location']
            timezone_info = weather_data['timezone_info']
            current_data = weather_data['current_data']
            forecast_data = weather_data['forecast_data']
            country = weather_data['country']
            flag_img = weather_data['flag_img']
            
            # Update UI with the fetched data
            temperature = current_data["main"]["temp"]
            humidity = current_data["main"]["humidity"]
            pressure = current_data["main"]["pressure"]
            windspeed = current_data["wind"]["speed"]
            cloud_description = current_data["weather"][0]["description"]
            
            # description of how the weather might feel like
            feels_like = current_data["main"]["feels_like"]
            desc = self.describe_feels_like(feels_like)
            
            # Update canvas text items with new weather data
            self.canvas.itemconfig(self.big_temp_text_id, text=f"{temperature}°C")
            self.canvas.itemconfig(self.humidity_text_id, text=f"Humidity:\n{humidity}%")
            self.canvas.itemconfig(self.pressure_text_id, text=f"Pressure:\n{pressure} hPa")
            self.canvas.itemconfig(self.windspeed_text_id, text=f"Windspeed:\n{windspeed} m/s")
            self.canvas.itemconfig(self.cloud_text_id, text=f"Clouds:\n{cloud_description.capitalize()}")
            self.canvas.itemconfig(self.feels_like_text_id, text=f"Feels like: {feels_like:.1f}°C — {desc}")

            # Load the images for the four weather parameters siting on frame 1
            self.pressure_icon = ImageTk.PhotoImage(Image.open("assets/images/pressure1.png"))
            self.humidity_icon = ImageTk.PhotoImage(Image.open("assets/images/humidity1.png"))
            self.wind_icon = ImageTk.PhotoImage(Image.open("assets/images/windspeed1.png"))
            self.description_icon = ImageTk.PhotoImage(Image.open("assets/images/cloud_description1.png"))
            self.big_temp_icon = ImageTk.PhotoImage(Image.open("assets/images/bigtemp2.png"))
            self.lonlat_icon = ImageTk.PhotoImage(Image.open("assets/images/lon_lat.png"))
            self.date_icon = ImageTk.PhotoImage(Image.open("assets/images/date.png"))
            self.time_icon = ImageTk.PhotoImage(Image.open("assets/images/time.png"))

            # Create the image on canvas with specified coordinates (x, y)
            self.pressure_img_id = self.canvas.create_image(480, 585,anchor="w", image=self.pressure_icon)
            self.humidity_img_id = self.canvas.create_image(160,585, anchor="w", image=self.humidity_icon)
            self.wind_img_id = self.canvas.create_image(750, 585, anchor="w", image=self.wind_icon)
            self.description_img_id = self.canvas.create_image(1050, 585, anchor="w", image=self.description_icon)
            self.big_temp_img_id = self.canvas.create_image(1090, 315, anchor="w", image=self.big_temp_icon)
            self.lonlat_img_id  = self.canvas.create_image(1110, 212, anchor="w", image=self.lonlat_icon)
            self.date_img_id  = self.canvas.create_image(40, 200, anchor="w", image=self.date_icon)
            self.time_img_id  = self.canvas.create_image(40, 110, anchor="w", image=self.time_icon)

            self.history_manager.save_search(city, temperature, humidity)
            
            # If history window exists, update it
            if hasattr(self, "history_window") and self.history_window.winfo_exists():
                self.update_history_window()

            # Update forecast data
            self.frame1 = ctk.CTkScrollableFrame(self, fg_color="#fff",
                                                orientation="horizontal")
            self.frame1.place(relwidth=0.84, relheight=0.25, relx=0.5, rely=0.98, anchor="s")

            for i in range(7):
                frame = ctk.CTkFrame(self.frame1, fg_color="lightblue")
                frame.pack(side="left", pady=10, padx=10, anchor="w")

                # Given date-time string
                date_str = forecast_data["list"][i]["dt_txt"]
                datetime_object = datetime.strptime(date_str, "%Y-%m-%d %H:%M:%S")
                formatted_date = datetime_object.strftime("%a %I:%M %p")
                tmp = forecast_data["list"][i]["main"]["temp"]

                # Placing labels at the top of frame1
                lbl = ctk.CTkLabel(frame, text=formatted_date, width=120, height=50, font=("Arial", 16, "bold"),
                                text_color="white", fg_color="black", corner_radius=20)
                lbl.pack(side="top", fill="x", padx=5, pady=5)  

                icon_code = forecast_data["list"][i]["weather"][0]["icon"]
                icon_path = f"assets/icon/{icon_code}@2x.png"

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

            # Update canvas text(geopy) items for location and time.
            self.canvas.itemconfig(self.country_id, text=f"{country}")
            self.canvas.itemconfig(self.city_name_id, text=f"{city}".capitalize())

            self.canvas.itemconfig(self.lonlat_text_id, text=f"{round(location.longitude, 2)}°E,{round(location.latitude, 2)}°N")
            self.canvas.itemconfig(self.time_text_id, text=f"{timezone_info['current_time']}")
            self.canvas.itemconfig(self.day_text_id, text=timezone_info['day'])
            self.canvas.itemconfig(self.date_text_id, text=timezone_info['date'])

            # Set flag image if available
            if flag_img:
                self.flag_img = ImageTk.PhotoImage(flag_img)
                self.canvas.itemconfig(self.flag_label, image=self.flag_img)
            else:
                self.canvas.itemconfig(self.flag_label, image="")

            # Check day/night and rain conditions
            sunrise = current_data["sys"]["sunrise"]
            sunset = current_data["sys"]["sunset"]
            timezone_offset = current_data["timezone"]
            
            rain_data = current_data.get("rain")  # Use .get() to avoid crash
            is_rain = rain_data is not None

            is_day = weather_fetcher.is_daytime(sunrise, sunset, timezone_offset)
            self.update_background(is_day, is_rain)  # Update the background image (day or night)
            self.toggle_mode(is_day)  # Update text colors based on day/night

        except Exception as e:
            CTkMessagebox(
                title="Error",
                message=f"Error fetching weather data: {str(e)}",
                icon="cancel",
                sound=True,
                bg_color="white",
                fg_color="lightblue",
                border_color="lightblue"
            )
        finally:
            self.stop_spinner()  # Stop the spinner after fetching data or if an error occurs
        
    def start_spinner(self):
        # Start the spinning dots animation
        self.spinner_active = True
        self.spinner_dots = []
        self.spinner_angle = 0

        # Define center and radius as instance variables
        self.center_x = 750
        self.center_y = 300 
        self.radius = 50  # Radius of the spinner circle


        dot_colors = ["#00FFFF", "#00D4FF", "#00AAFF", "#008CFF","#006EFF", "#004C99", "#003366", "#001F4D"]


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
        #Animate the spinning dots
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
        #Stop the spinning dots animation
        self.spinner_active = False
        for dot in self.spinner_dots:
            self.canvas.delete(dot)
        self.spinner_dots = []


    def initialize_weather_map(self):
        # Create frame for the map
        self.map_frame = ctk.CTkFrame(self, fg_color="white", corner_radius=10)

        # Create the map widget
        self.map_widget = TkinterMapView(self.map_frame, width=600, height=400, corner_radius=10)
        self.map_widget.pack(fill="both", expand=True, padx=5, pady=5)

        # Set default position (Accra, Ghana) and zoom level
        self.map_widget.set_position(5.6037, -0.1870)
        self.map_widget.set_zoom(10)  # More reasonable zoom level for city view

        # Add right-click menu to search weather at clicked location
        self.map_widget.add_right_click_menu_command(
            label="Search Weather Here",
            command=self.map_click_callback,
            pass_coords=True
        )

        # Add marker for current location
        self.current_marker = None

    def map_click_callback(self, coords):
        lat, lon = coords
        
        # Clear previous marker
        if self.current_marker:
            self.map_widget.delete(self.current_marker)
        
        # Add new marker
        self.current_marker = self.map_widget.set_marker(lat, lon)
        self.map_widget.set_position(lat, lon)
        
        # OpenWeather Reverse Geocoding API
        url = f"http://api.openweathermap.org/geo/1.0/reverse?lat={lat}&lon={lon}&limit=1&appid={self.API_KEY}"
        
        try:
            response = requests.get(url)
            data = response.json()
            
            if data and isinstance(data, list):
                city = data[0].get("name", "Unknown")
                country = data[0].get("country", "")
                
                print(f"OpenWeather Geocoding Result: {city}, {country}")
                
                self.search_entry.delete(0, "end")
                self.search_entry.insert(0, city)
                self.getweather()
            else:
                CTkMessagebox(
                    title="Error",
                    message="No location data found for these coordinates.",
                    icon="warning"
                )
        
        except Exception as e:
            print(f"OpenWeather Geocoding Error: {str(e)}")
            CTkMessagebox(
                title="Error",
                message=f"Geocoding failed: {str(e)}",
                icon="cancel"
            )

    def toggle_map(self):
        if self.map_visible:
            self.map_frame.place_forget()
            self.map_button.configure(text="🌍 Show Map")
        else:
            self.map_frame.place(relx=0.2, rely=0.25, relwidth=0.5, relheight=0.3,)
            self.map_button.configure(text="🗺️ Hide Map")
        
        self.map_visible = not self.map_visible

        
if __name__ == "__main__":
    app = WeatherApp()
    app.mainloop()