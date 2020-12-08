from http import HTTPStatus

from fastapi import FastAPI
from fastapi.logger import logger

from weather_api.cache import get_cache
from weather_api.owm_client import OWMRestClient

api = FastAPI()
api.cache = get_cache()


@api.get("/forecast")
async def get_forecast(city):
    cached_data = api.cache.get(city)
    if cached_data:
        return cached_data
    owm = OWMRestClient()
    weather = await owm.get_by_city(city)
    if weather.status != HTTPStatus.OK:
        if weather.status == HTTPStatus.NOT_FOUND:
            return {"status": HTTPStatus.NOT_FOUND, "data": "City not found"}
        logger.error(
            f"Unsuccessful response from OWM. Status: {weather.status}. Response: {weather.data}"
        )
        raise ApiException("Something went wrong")
    response = {
        "status": HTTPStatus.OK,
        "data": {
            "city": {
                "coord": weather.data["coord"],
                "country": weather.data["sys"]["country"],
            },
            "temp": f'{weather.data["main"]["temp"]} Cº',
            "temp_min": f'{weather.data["main"]["temp_min"]} Cº',
            "temp_max": f'{weather.data["main"]["temp_max"]} Cº',
            "feels": f'{weather.data["main"]["feels_like"]} Cº',
            "pressure": f'{weather.data["main"]["pressure"]} Hg',
            "humidity": f'{weather.data["main"]["humidity"]}%',
            "wind_speed": f'{weather.data["wind"]["speed"]} m/s',
        },
    }
    api.cache.set(city, response)
    return response


class ApiException(Exception):
    pass
