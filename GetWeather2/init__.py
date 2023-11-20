import logging
import azure.functions as func
import requests

def main(req: func.HttpRequest) -> func.HttpResponse:
    logging.info('Python HTTP trigger function processed a request.')

    city = req.params.get('city')
    if not city:
        return func.HttpResponse(
             "Please provide a 'city' parameter in the query string.",
             status_code=400
        )

    api_key = "31061e71138b8a05356fba63f13034f8"
    url = "https://api.openweathermap.org/data/2.5/weather"
    params = {"q": city, "appid": api_key, "units": "metric"}

    response = requests.get(url, params=params)

    if response.status_code == 200:
        weather_data = response.json()
        temperature = weather_data['main']['temp']
        description = weather_data['weather'][0]['description']
        humidity = weather_data['main']['humidity']
        
        result = {
            "Town": city,
            "Temperature": f"{temperature}°C",
            "Description": description,
            "Humidity": f"{humidity}%"
        }
        return func.HttpResponse(
            body=str(result),
            mimetype="application/json",
            status_code=200
        )
    else:
        return func.HttpResponse(
            f"Failed to retrieve weather data for {city}.",
            status_code=500
        )
