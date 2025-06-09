🌦️ Weather Forecast App
A sleek desktop weather app built with Python and CustomTkinter, fetching real-time data from OpenWeatherMap, Geopy, and TimezoneFinder. 
Features interactive maps, animated icons, and city search with auto-suggestions.

🚀 Key Features
🔍 Search by city with auto-suggestions

📊 Current weather: Temperature, humidity, wind speed, and conditions

🗺️ Interactive map (via tkintermapview)

🌈 Lottie animations for dynamic weather icons

⏰ Real-time timezone and location handling

📜 Search history tracking

🛠️ Tech Stack
Language: Python 3.x

GUI: CustomTkinter (modern UI)

APIs:

  ...OpenWeatherMap (weather data).....get your api key from OpenWeatherMap and save in a .env file

  ...Geopy (geocoding)

 ...TimezoneFinder (timezone detection)

Map: tkintermapview (interactive maps)

Animations: Lottie JSON files

⚙️ Installation
1. Clone the repository
bash
git clone https://github.com/1efferson/weatherapp.git
cd weatherapp
2. Set up the virtual environment

Windows:
venv\Scripts\activate

macOS/Linux:
source venv/bin/activate

3. Install dependencies
bash
pip install -r requirements.txt

4. Restart VSCode (Critical!)
🚨 Before launching the app, restart VSCode to ensure all dependencies and environment paths are loaded correctly.

5. Run the app
bash
python WeatherApp_main.py

❓ Troubleshooting
If the app crashes or dependencies aren’t detected, restart VSCode and re-activate the virtual environment.

Ensure your API keys (OpenWeatherMap) are properly configured in the app.



A view of the APP.......![Audio Recognition](assets/Audio_recognition_feature.png)


