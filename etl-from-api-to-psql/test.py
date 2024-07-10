import json
import requests as req
from geopy import geocoders

TOKEN_YANDEX = "80a4c74c-d6a7-4d51-ab31-e3d850aee839"


def geo_pos(city: str):
    """
    Retrieve the geographical coordinates (latitude and longitude) of the given city.

    Parameters:
    - city: a string representing the name of the city

    Return: a tuple containing the latitude and longitude of the city, or None if the coordinates cannot be retrieved
    """
    geolocator = geocoders.Nominatim(user_agent="YaTest")
    location = geolocator.geocode(city)
    if location:
        latitude = location.latitude
        longitude = location.longitude
        return latitude, longitude
    else:
        print(f"Failed to retrieve coordinates for {city}")
        return None


def yandex_weather(latitude: float, longitude: float, token_yandex: str):
    """
    Sends a request to the Yandex Weather API using the provided latitude, longitude, and Yandex API token.
    Returns the weather forecast data in JSON format.
    """
    url_yandex = f"https://api.weather.yandex.ru/v2/forecast/"
    params = {"lat": latitude, "lon": longitude, "lang": "ru_RU"}
    headers = {"X-Yandex-API-Key": token_yandex}
    yandex_req = req.get(url_yandex, headers=headers, params=params)
    if yandex_req.status_code != 200:
        print(f"Error {yandex_req.status_code} in request")
        return None
    yandex_json = yandex_req.json()

    return yandex_json


def convert_to_csv(city: str, forecast_data):
    """
    Convert the forecast data for a given city into a CSV format.

    Parameters:
    - city: the name of the city for which the forecast data is being converted
    - forecast_data: the forecast data containing information about the weather

    Returns:
    A list of lists representing the CSV rows, each containing city, date, hour, temperature in Celsius, pressure in mm, rainy indicator, and condition
    """
    csv_rows = []

    for forecast in forecast_data["forecasts"]:
        date = forecast["date"]
        if "hours" not in forecast:
            continue

        for hour_data in forecast["hours"]:
            hour = hour_data["hour"]
            temperature_c = hour_data.get("temp", "N/A")
            pressure_mm = hour_data.get("pressure_mm", "N/A")
            is_rainy = 1 if hour_data.get("prec_mm", 0) > 0 else 0
            condition = hour_data.get("condition", "N/A")

            row = [city, date, hour, temperature_c, pressure_mm, is_rainy, condition]
            csv_rows.append(row)

    return csv_rows


def main():
    """
    A function to collect weather data for a list of cities and save it in a CSV file.
    """
    csv_rows = []
    cities = [
        {
            "name": "Moscow",
        },
        {
            "name": "Kazan",
        },
        {
            "name": "Saint Petersburg",
        },
        {
            "name": "Tula",
        },
        {
            "name": "Novosibirsk",
        },
    ]

    for city in cities:
        # Получаем координаты для города
        coordinates = geo_pos(city["name"])

        if coordinates:
            latitude, longitude = coordinates
            # Получаем данные о погоде для города
            weather_data = yandex_weather(latitude, longitude, TOKEN_YANDEX)
            if weather_data:
                # Преобразуем данные о погоде в CSV формат
                city_rows = convert_to_csv(city["name"], weather_data)
                csv_rows.extend(city_rows)

    # Записываем данные в CSV файл
    with open("weather_data.csv", "w", newline="", encoding="utf-8") as csv_file:
        csv_header = [
            "city",
            "date",
            "hour",
            "temperature_c",
            "pressure_mm",
            "is_rainy",
            "condition",
        ]
        csv_writer = csv.writer(csv_file)
        csv_writer.writerow(csv_header)
        csv_writer.writerows(csv_rows)
