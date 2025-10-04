from flask import Flask, request, render_template
import requests as req
from datetime import datetime

app = Flask(__name__)
api = "0a4756309e70131e9c6ed76856e2fa5f"

# Example country to city mapping (expand this as needed)
country_cities = {
    "US": ["New York", "Los Angeles", "Chicago", "Houston", "Miami"],
    "FR": ["Paris", "Lyon", "Marseille", "Toulouse", "Nice"],
    "GB": ["London", "Manchester", "Birmingham", "Leeds", "Glasgow"],
    # Add more countries and cities here
}

@app.route('/', methods=["GET", "POST"])
def index():
    weather = None
    selected_city = ""
    selected_country = ""
    selected_time = ""

    if request.method == "POST":
        selected_city = request.form["city"]
        selected_country = request.form["iso2"]
        selected_time = request.form["time"]

        url = "https://api.openweathermap.org/data/2.5/forecast"
        params = {"q": f"{selected_city},{selected_country}", "appid": api, "units": "metric"}
        res = req.get(url, params=params)
        data = res.json()

        if res.status_code == 200:
            try:
                time_obj = datetime.strptime(selected_time, "%Y-%m-%d %H:%M")
                closest = min(
                    data['list'],
                    key=lambda f: abs(datetime.fromtimestamp(f["dt"]) - time_obj),
                )
                forecast_time = datetime.fromtimestamp(closest["dt"])
                temp = closest["main"]["temp"]
                description = closest["weather"][0]["description"]
                rain = closest.get("rain", {}).get("3h", 0)
                weather = {
                    "city": selected_city,
                    "country": selected_country,
                    "forecast_time": forecast_time.strftime("%Y-%m-%d %H:%M"),
                    "temp": temp,
                    "description": description,
                    "rain": f"{rain}mm in last 3h" if rain else "No rain"
                }
            except Exception as e:
                weather = {"description": f"Error: {str(e)}"}
        else:
            weather = {"description": f"API Error: {data.get('message', 'Unknown')}"}

    return render_template(
        "index.html",
        weather=weather,
        selected_city=selected_city,
        selected_country=selected_country,
        selected_time=selected_time,
        country_cities=country_cities
    )

@app.route("/support")
def support():
    return render_template("support.html")

if __name__ == "__main__":
    app.run(debug=True)
