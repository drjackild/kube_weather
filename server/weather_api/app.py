from http import HTTPStatus
from typing import cast

from fastapi import FastAPI, Response
from fastapi.logger import logger

from weather_api.cache import InMemoryCache, get_cache
from weather_api.owm_client import OWMRestClient

from . import settings


class WeatherAPI(FastAPI):
    cache: InMemoryCache


api = WeatherAPI()
api.cache = get_cache(settings.CACHE_TTL)


@api.get("/forecast")
async def get_forecast(city: str) -> dict:
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
    data = weather.data
    data = cast(dict, data)
    response = {
        "status": HTTPStatus.OK,
        "data": {
            "city": {
                "coord": data["coord"],
                "country": data["sys"]["country"],
            },
            "temp": f"{data['main']['temp']} Cº",
            "temp_min": f"{data['main']['temp_min']} Cº",
            "temp_max": f"{data['main']['temp_max']} Cº",
            "feels": f"{data['main']['feels_like']} Cº",
            "pressure": f"{data['main']['pressure']} Hg",
            "humidity": f"{data['main']['humidity']}%",
            "wind_speed": f"{data['wind']['speed']} m/s",
        },
    }
    api.cache.set(city, response)
    return response


@api.get("/health")
async def health() -> Response:
    return Response(status_code=HTTPStatus.OK)


class ApiException(Exception):
    pass
