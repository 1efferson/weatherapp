
import customtkinter as ctk
from geopy.geocoders import Nominatim
from CTkMessagebox import CTkMessagebox
from timezonefinder import TimezoneFinder
from datetime import *
import requests
import pytz
from PIL import Image
import certifi
import ssl




# Set dark theme
ctk.set_appearance_mode("light")  # Options: "dark", "light", "system"
ctk.set_default_color_theme("green")  # You can try other themes like "blue" or "green"

class WeatherApp(ctk.CTk):
    def __init__(self): 
        super().__init__()
        self.geometry("1200x700")
        self.title("WEATHER FORECAST APPLICATION")
        


        # Creating a frame for the forecast for the days of the week
        self.frame1 = ctk.CTkFrame(self,fg_color="#fff", corner_radius=20)
        self.frame1.place(relwidth=0.8, relheight=0.25, relx=0.5, rely=1.0, anchor="s")

        # Adding 7 labels to self.frame1 using .place
        days = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"]
        x_positions = [30, 210, 390, 570, 750, 930, 1110]  # Custom x-coordinates for label placement
        for i, day in enumerate(days):
            label = ctk.CTkLabel(self.frame1, text=day, width=100, height=50, font=("Arial", 12, "bold"), text_color="white", fg_color="black")
            label.place(x=x_positions[i], y=10)  # Placing labels at the top of frame1

        # label for Big temperature value on the right 
        Big_Temp_number = ctk.CTkLabel(self,text="Big Temp value",font=("Arial", 12, "bold"), fg_color="white",text_color="black", corner_radius=20)
        Big_Temp_number.place(relwidth=0.2, relheight=0.3, relx=0.7, rely=0.2)
 

        #the 3 labels on the left of the app window
        time_label = ctk.CTkLabel(self, text="time", width=100, height=20,font=("Arial", 12, "bold"), text_color="black", fg_color="#fff",corner_radius=20)
        time_label.place(relwidth=0.1, relheight=0.1, relx=0.1, rely=0.08)

        day_label = ctk.CTkLabel(self, text="day", width=100, height=20,font=("Arial", 12, "bold"), text_color="black", fg_color="#fff",corner_radius=20)
        day_label.place(relwidth=0.1, relheight=0.06, relx=0.1, rely=0.2)

        date_label = ctk.CTkLabel(self, text="Date", width=100, height=20,font=("Arial", 12, "bold"), text_color="black", fg_color="#fff",corner_radius=20)
        date_label.place(relwidth=0.1, relheight=0.06, relx=0.1, rely=0.3)

        time_zone_label = ctk.CTkLabel(self, text="time zone", width=100, height=20,font=("Arial", 12, "bold"), text_color="black", fg_color="#fff",corner_radius=20)
        time_zone_label.place(relwidth=0.1, relheight=0.06, relx=0.1, rely=0.4)

        longitude_latitude_label = ctk.CTkLabel(self, text="long/lat", width=100, height=20,font=("Arial", 12, "bold"), text_color="black", fg_color="#fff",corner_radius=20)
        longitude_latitude_label.place(relwidth=0.1, relheight=0.06, relx=0.1, rely=0.5)

#labels for other weather conditions on top of the frame1

        humidity_label = ctk.CTkLabel(self, text="humidity", width=100, height=20, 
                                        font=("Arial", 12, "bold"), text_color="black", fg_color="#fff",corner_radius=20)
        humidity_label.place(relwidth=0.1, relheight=0.1, relx=0.12, rely=0.6)

        pressure_label = ctk.CTkLabel(self, text="pressure", width=100, height=20, 
                                      font=("Arial", 12, "bold"), text_color="black", fg_color="#fff",corner_radius=20)
        pressure_label.place(relwidth=0.1, relheight=0.1, relx=0.25, rely=0.6)

        windspeed_label = ctk.CTkLabel(self, text="windspeed", width=100, height=20, 
                                      font=("Arial", 12, "bold"), text_color="black", fg_color="#fff",corner_radius=20)
        windspeed_label.place(relwidth=0.1, relheight=0.1, relx=0.38, rely=0.6)

        cloud_status_label = ctk.CTkLabel(self, text="cloud status", width=100, height=20, 
                                      font=("Arial", 12, "bold"), text_color="black", fg_color="#fff",corner_radius=20)
        cloud_status_label.place(relwidth=0.1, relheight=0.1, relx=0.51, rely=0.6)

        miscillamous1_label = ctk.CTkLabel(self, text="to be determined", width=100, height=20, 
                                      font=("Arial", 12, "bold"), text_color="black", fg_color="#fff",corner_radius=20)
        miscillamous1_label.place(relwidth=0.1, relheight=0.1, relx=0.64, rely=0.6)

        miscillamous2_label = ctk.CTkLabel(self, text="to be determined", width=100, height=20, 
                                      font=("Arial", 12, "bold"), text_color="black", fg_color="#fff",corner_radius=20)
        miscillamous2_label.place(relwidth=0.1, relheight=0.1, relx=0.77, rely=0.6)

        # current current_city label 
        current_city= ctk.CTkLabel(self, text="current city", font=("Arial", 12, "bold"), text_color="black", fg_color="#fff",corner_radius=20)
        current_city.place(relwidth=0.2, relheight=0.06, relx=0.7, rely=0.1)        


#creating a frame for the searchbar to put the two images inside of it
        # Create a frame to contain the images and text
        searchbar_frame = ctk.CTkFrame(self, fg_color="white", corner_radius=20)
        searchbar_frame.place(relwidth=0.3, relheight=0.05, relx=0.3, rely=0.1)

        # Load images using CTkImage
        searchbar_cloud_image = ctk.CTkImage(light_image=Image.open("images/searchbar_cloud1.png"), size=(30, 30))
        searchbar_search_image = ctk.CTkImage(light_image=Image.open("images/search_icon.png"), size=(30, 30))

        # Left-side image
        left_label_in_searchbar = ctk.CTkLabel(searchbar_frame, image=searchbar_cloud_image, text="", fg_color="transparent")
        left_label_in_searchbar.pack(side="left", padx=5, pady=5)
        
        #add an entry box to the search bar
        search_entry = ctk.CTkEntry(searchbar_frame, font=("Arial", 12), text_color="black",placeholder_text="Search City Here",placeholder_text_color="blue", fg_color="white", border_width=0)
        search_entry.pack(side="left", expand=True, fill="both", padx=5)
        search_entry.focus()  # Auto-focus on entry field

        # Search button with for the Right-side search image
        search_button = ctk.CTkButton(searchbar_frame,image=searchbar_search_image,text="", fg_color="white",hover_color="lightgrey",width=20, height=20,command="")
        search_button.pack(side="right", padx=5, pady=5)



if __name__ == "__main__":
    app = WeatherApp()
    app.mainloop()














