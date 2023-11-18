import azure.functions as func
import requests
import json
import os

def main(req: func.HttpRequest) -> func.HttpResponse:
    city = req.params.get('city')

    if not city:
        return func.HttpResponse(
            "Please pass a city in the query string",
            status_code=400
        )

    api_key = os.environ.get('OpenWeatherMapApiKey')
    url = "https://api.openweathermap.org/data/2.5/weather"
    params = {"q": city, "appid": api_key, "units": "metric"}

    response = requests.get(url, params=params)

    if response.status_code == 200:
        weather_data = response.json()
        return func.HttpResponse(json.dumps(weather_data), mimetype="application/json")
    else:
        return func.HttpResponse(
            "Failed to fetch the weather data",
            status_code=response.status_code
        )
