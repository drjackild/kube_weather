import typing as t
from http import HTTPStatus
from json.decoder import JSONDecodeError
from urllib.parse import urljoin, urlencode

from aiohttp import ContentTypeError
from aiohttp.client import ClientSession
from fastapi.logger import logger

from server.weather_api import settings

HTTP_METHOD = t.Literal["GET"]


class ApiMethods:
    get: t.Literal["GET"] = "GET"


class RestClientResponse:
    def __init__(self, data: t.Union[str, dict], status: int):
        self.data = data
        self.status = status


class OneCallResultSet:
    CHOICES = t.Literal["current", "minutely", "hourly", "daily", "alerts"]

    current: t.Literal["current"] = "current"
    minutely: t.Literal["minutely"] = "minutely"
    hourly: t.Literal["hourly"] = "hourly"
    daily: t.Literal["daily"] = "daily"
    alerts: t.Literal["alerts"] = "alerts"


class OWMRestClient:
    base_url = "https://api.openweathermap.org/data/2.5/"

    async def onecall(
        self,
        lat: float,
        lon: float,
        exclude: t.Optional[t.Iterable[OneCallResultSet.CHOICES]] = None,
    ) -> RestClientResponse:
        params = {"lat": lat, "lon": lon, "appid": settings.OWM_API_KEY}
        if exclude:
            params["exclude"] = ",".join(exclude)
        uri = f"onecall?{urlencode(params)}"
        response = await self._make_request(uri, method=ApiMethods.get)
        if response.status != HTTPStatus.OK:
            raise RestClientException(
                f"Unsuccessful request to /onecal. Respone: {response.data}"
            )
        return response

    async def _make_request(
        self, uri: str, method: HTTP_METHOD, headers: t.Optional[dict] = None,
    ):
        url = urljoin(self.base_url, uri)
        logger.debug(f"{method} {url}: request")
        async with ClientSession() as session:
            if method == ApiMethods.get:
                r = await session.get(url, headers=headers)
                try:
                    response = RestClientResponse(await r.json(), r.status)
                except ContentTypeError:
                    response = RestClientResponse(await r.text(), r.status)
            else:
                raise RestClientException(f"Invalid API method: {method}")
        logger.debug(f"{method} {url}: status: {r.status}")
        return response


class RestClientException(Exception):
    pass
