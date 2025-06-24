<h1 align="center">🌦️ Weather Forecast App</h1>

<p align="center" style="font-size: 18px; max-width: 800px; margin: auto;">
  A sleek desktop weather app built with <strong>Python</strong> and <strong>CustomTkinter</strong>, fetching real-time data from <em>OpenWeatherMap</em>, <em>Geopy</em>, and <em>TimezoneFinder</em>. Features interactive maps, animated icons, and city search with auto-suggestions.
</p>

<hr/>

<h2>A Preview of the APP</h2>

.......![Audio Recognition](Assets/images/Audio_recognition_feature.png)

![City Auto Suggestion](Assets/images/City_auto_suggestion_feature.png)

![Map Search Functionality](Assets/images/Map_search_functionality.png)
<hr/>

<h2>🚀 Key Features</h2>
<ul>
  <li>🔍 <strong>Search by city</strong> with auto-suggestions</li>
  <li>📊 <strong>Current weather</strong>: Temperature, humidity, wind speed, and conditions</li>
  <li>🗺️ <strong>Interactive map</strong> (via <code>tkintermapview</code>)</li>
  <li>🌈 <strong>Lottie animations</strong> for dynamic weather icons</li>
  <li>⏰ <strong>Real-time timezone</strong> and location handling</li>
  <li>📜 <strong>Search history tracking</strong></li>
</ul>

<h2>🛠️ Tech Stack</h2>
<ul>
  <li><strong>Language</strong>: Python 3.x</li>
  <li><strong>GUI</strong>: CustomTkinter (modern UI)</li>
  <li><strong>APIs</strong>:
    <ul>
      <li>🌤️ OpenWeatherMap (weather data) — <em>Get your API key and save it in a <code>.env</code> file</em></li>
      <li>📍 Geopy (geocoding)</li>
      <li>🕒 TimezoneFinder (timezone detection)</li>
    </ul>
  </li>
  <li><strong>Map</strong>: tkintermapview (interactive maps)</li>
  <li><strong>Animations</strong>: Lottie JSON files</li>
</ul>

<h2>⚙️ Installation</h2>

<ol>
  <li>Clone the repository:
    <pre><code>git clone https://github.com/1efferson/weatherapp.git
cd weatherapp</code></pre>
  </li>
  <li>Set up the virtual environment:

  <pre><code> # macOS/Linux
source venv/bin/activate</code></pre>

  <pre><code># Window
venv\Scripts\activate

 
  </li>
  <li>Install dependencies:
    <pre><code>pip install -r requirements.txt</code></pre>
  </li>
  <li><strong>🚨 Restart VSCode</strong> before launching the app to ensure all dependencies and environment paths are loaded correctly.</li>
  <li>Run the app:
    <pre><code>python WeatherApp_main.py</code></pre>
  </li>
</ol>

<h2>❓ Troubleshooting</h2>
<ul>
  <li>If the app crashes or dependencies aren’t detected, restart VSCode and re-activate the virtual environment.</li>
  <li>Ensure your API keys (OpenWeatherMap) are properly configured in the app.</li>
</ul>



<h2>📌 Known Issue</h2>

<div style="background-color: #fff3cd; border-left: 6px solid #ffecb5; padding: 12px; margin-bottom: 20px;">
  <p><strong>⚠️ Background Image Responsiveness on Windows</strong></p>
  <p>Currently, the app's background image does <strong>not resize correctly on Windows</strong> systems. This is a known issue and is actively being worked on to ensure full cross-platform compatibility.</p>
</div>

<h2>🤝 Contribute & Collaborate</h2>

<p>I welcome contributions and collaborations! If you're interested in improving or extending the app:</p>

<ul>
  <li>🍴 <strong>Fork</strong> the repository</li>
  <li>📥 <strong>Open a pull request</strong> with your improvements</li>
  <li>💬 Or simply <strong>open an issue</strong> to suggest ideas</li>
</ul>

<p><strong>Let’s build something great together!</strong> 🚀</p>








