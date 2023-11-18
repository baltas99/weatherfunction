import azure.functions as func
import requests
import json

def main(req: func.HttpRequest) -> func.HttpResponse:
    # Extract the city name from the query parameters
    city = req.params.get('city')

    if not city:
        return func.HttpResponse(
            "Please pass the city name in the query string",
            status_code=400
        )

    # Set your OpenWeatherMap API key
    api_key = "31061e71138b8a05356fba63f13034f8"
    # Define the base URL for the OpenWeatherMap API
    url = "https://api.openweathermap.org/data/2.5/weather"
    # Set the parameters for the API call
    params = {"q": city, "appid": api_key, "units": "metric"}

    # Make the API call to OpenWeatherMap
    response = requests.get(url, params=params)

    if response.status_code == 200:
        weather_data = response.json()
        # Create a response object with the weather data
        weather_response = {
            "Town": city,
            "Temperature": f"{weather_data['main']['temp']}°C",
            "Description": weather_data['weather'][0]['description'],
            "Humidity": f"{weather_data['main']['humidity']}%"
        }
        return func.HttpResponse(json.dumps(weather_response), mimetype="application/json")
    else:
        return func.HttpResponse(
            f"Failed to fetch the weather data for {city}.",
            status_code=response.status_code
        )
