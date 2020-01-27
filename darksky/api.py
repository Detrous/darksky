from datetime import datetime

import aiohttp

from .forecast import Forecast
from .request_manager import (BaseRequestManger, RequestManger,
                              RequestMangerAsync)
from .types import languages, units, weather


class BaseDarkSky:
    HOST = "https://api.darksky.net/forecast"

    def __init__(self, api_key: str):
        self.api_key: str = api_key
        self.request_manager: BaseRequestManger = None

    def get_forecast(
        self,
        latitude: float,
        longitude: float,
        extend: bool = None,
        lang=languages.ENGLISH,
        values_units=units.AUTO,
        exclude: [weather] = None,
        timezone: str = None,
    ):
        raise NotImplementedError

    def get_time_machine_forecast(
        self,
        latitude: float,
        longitude: float,
        time: datetime,
        extend: bool = False,
        lang=languages.ENGLISH,
        values_units=units.AUTO,
        exclude: [weather] = None,
        timezone: str = None,
    ):
        raise NotImplementedError

    def get_url(self, latitude: float, longitude: float, time=None, **params):
        if time is None:
            return "{host}/{api_key}/{latitude},{longitude}".format(
                api_key=self.api_key,
                host=self.HOST,
                latitude=latitude,
                longitude=longitude,
            )
        return "{host}/{api_key}/{latitude},{longitude},{time}".format(
            api_key=self.api_key,
            host=self.HOST,
            latitude=latitude,
            longitude=longitude,
            time=time,
        )


class DarkSky(BaseDarkSky):
    def __init__(self, api_key: str, gzip: bool = True):
        super().__init__(api_key)
        self.request_manager = RequestManger(gzip)

    def get_forecast(
        self,
        latitude: float,
        longitude: float,
        extend: bool = None,
        lang=languages.ENGLISH,
        values_units=units.AUTO,
        exclude: [weather] = None,
        timezone: str = None,
    ) -> Forecast:
        url = self.get_url(latitude, longitude)
        data = self.request_manager.make_request(
            url=url,
            extend=weather.HOURLY if extend else None,
            lang=lang,
            units=values_units,
            exclude=exclude,
            timezone=timezone,
        )
        return Forecast(**data)

    def get_time_machine_forecast(
        self,
        latitude: float,
        longitude: float,
        time: datetime,
        extend: bool = False,
        lang=languages.ENGLISH,
        values_units=units.AUTO,
        exclude: [weather] = None,
        timezone: str = None,
    ) -> Forecast:
        url = self.get_url(latitude, longitude, int(time.timestamp()))
        data = self.request_manager.make_request(
            url=url,
            extend=weather.HOURLY if extend else None,
            lang=lang,
            units=values_units,
            exclude=exclude,
            timezone=timezone,
        )
        return Forecast(**data)


class DarkSkyAsync(BaseDarkSky):
    def __init__(
        self,
        api_key: str,
        gzip: bool = True,
        client_session: aiohttp.ClientSession = None,
    ):
        super().__init__(api_key)
        self.request_manager = RequestMangerAsync(
            gzip=gzip, client_session=client_session
        )

    async def get_forecast(
        self,
        latitude: float,
        longitude: float,
        extend: bool = None,
        lang=languages.ENGLISH,
        values_units=units.AUTO,
        exclude: [weather] = None,
        timezone: str = None,
    ) -> Forecast:
        url = self.get_url(latitude, longitude)
        data = await self.request_manager.make_request(
            url=url,
            extend=weather.HOURLY if extend else None,
            lang=lang,
            units=values_units,
            exclude=exclude,
            timezone=timezone,
        )
        return Forecast(**data)

    async def get_time_machine_forecast(
        self,
        latitude: float,
        longitude: float,
        time: datetime,
        extend: bool = False,
        lang=languages.ENGLISH,
        values_units=units.AUTO,
        exclude: [weather] = None,
        timezone: str = None,
    ) -> Forecast:
        url = self.get_url(latitude, longitude, int(time.timestamp()))
        data = await self.request_manager.make_request(
            url=url,
            extend=weather.HOURLY if extend else None,
            lang=lang,
            units=values_units,
            exclude=exclude,
            timezone=timezone,
        )
        return Forecast(**data)
