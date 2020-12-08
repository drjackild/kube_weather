import asyncio
import typing as t
from dataclasses import dataclass
from urllib.parse import urlencode, urljoin

from aiohttp import ContentTypeError
from aiohttp.client import ClientSession
from fastapi.logger import logger

from . import settings

HTTP_METHOD = t.Literal["GET"]


class ApiMethods:
    get: t.Literal["GET"] = "GET"


class RestClientResponse:
    def __init__(self, data: t.Union[str, dict], status: int):
        self.data = data
        self.status = status

    def __repr__(self):
        return f"{self.__class__.__name__} <{self.status}>"


@dataclass
class RetryPolicy:
    attempts: int
    start_interval: float
    step: float


class OWMRestClient:
    class Units:
        CHOICES = t.Literal["standard", "metric", "imperial"]

        standard: t.Literal["standard"] = "standard"
        metric: t.Literal["metric"] = "metric"
        imperial: t.Literal["imperial"] = "imperial"

    class OneCallField:
        CHOICES = t.Literal["current", "minutely", "hourly", "daily", "alerts"]

        current: t.Literal["current"] = "current"
        minutely: t.Literal["minutely"] = "minutely"
        hourly: t.Literal["hourly"] = "hourly"
        daily: t.Literal["daily"] = "daily"
        alerts: t.Literal["alerts"] = "alerts"

    base_url = "https://api.openweathermap.org/data/2.5/"
    default_retry_policy = RetryPolicy(attempts=3, step=2, start_interval=1)

    def __init__(
        self,
        retry_policy: t.Optional[RetryPolicy] = None,
        retry_statuses: t.Optional[t.List] = None,
    ):
        self.retry_policy = retry_policy or self.default_retry_policy
        self.retry_statuses = retry_statuses or [500]

    async def get_by_city(
        self,
        city: str,
        units: Units.CHOICES = Units.metric,
    ):
        params = {"q": city, "appid": settings.OWM_API_KEY, "units": units}
        uri = f"weather?{urlencode(params)}"
        response = await self._make_request(uri, method=ApiMethods.get)
        return response

    async def onecall(
        self,
        lat: float,
        lon: float,
        units: Units.CHOICES = Units.metric,
        exclude: t.Optional[t.Iterable[OneCallField.CHOICES]] = None,
    ) -> RestClientResponse:
        params = {"lat": lat, "lon": lon, "appid": settings.OWM_API_KEY, "units": units}
        if exclude:
            params["exclude"] = ",".join(exclude)
        uri = f"onecall?{urlencode(params)}"
        response = await self._make_request(uri, method=ApiMethods.get)
        return response

    async def _make_request(
        self,
        uri: str,
        method: HTTP_METHOD,
        headers: t.Optional[dict] = None,
    ) -> RestClientResponse:
        url = urljoin(self.base_url, uri)
        logger.debug(f"{method} {url}: request")

        async with ClientSession() as session:

            async def _retry_circle(session_method: t.Callable, **kwargs):
                interval = self.retry_policy.start_interval
                for i in range(0, self.retry_policy.attempts):
                    await asyncio.sleep(interval)
                    logger.warning(
                        f"Retry {i+1}/{self.retry_policy.attempts} ({interval}s): {kwargs.get('url')}"
                    )
                    r = await session_method(**kwargs)
                    if r.status not in self.retry_statuses:
                        return r
                    interval += self.retry_policy.step
                else:
                    raise RestClientException(
                        f"Request failed. Status: {r.status}. Response: {await r.text()}"
                    )

            if method == ApiMethods.get:
                r = await session.get(url, headers=headers)
                if r.status in self.retry_statuses:
                    r = await _retry_circle(session.get, url=url, headers=headers)
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
