import requests
from datetime import datetime

from .forecast import Forecast
from .exceptions import DarkSkyException
from .types import languages, units, weather
from .request_manager import BaseRequestManger, RequestManger, RequestMangerAsync


class BaseDarkSky(object):
    HOST = 'https://api.darksky.net/forecast'

    request_manager_class = BaseRequestManger

    def __init__(self, api_key, gzip: bool=True):
        self.api_key = api_key
        self.request_manager = self.request_manager_class(gzip)

    def get_forecast(self, 
        latitude: float, longitude: float, extend: bool=None, lang=languages.ENGLISH, 
        units=units.AUTO, exclude: [weather]=None):
        raise NotImplementedError

    def get_time_machine_forecast(
        self, latitude: float, longitude: float, time: datetime, extend: bool=False, 
        lang=languages.ENGLISH, units=units.AUTO, exclude: [weather]=None):
        raise NotImplementedError

    def get_url(self, latitude: float, longitude: float, time=None, **params):
        if time is None:
            return '{host}/{api_key}/{latitude},{longitude}'.format(
                api_key=self.api_key,
                host=self.HOST,
                latitude=latitude,
                longitude=longitude
            )
        else: 
            return '{host}/{api_key}/{latitude},{longitude},{time}'.format(
                api_key=self.api_key,
                host=self.HOST,
                latitude=latitude,
                longitude=longitude,
                time=time
            )


class DarkSky(BaseDarkSky):
    HOST = 'https://api.darksky.net/forecast'

    request_manager_class = RequestManger

    def get_forecast(self, 
        latitude: float, longitude: float, extend: bool=None, lang=languages.ENGLISH, 
        units=units.AUTO, exclude: [weather]=None):
        url = self.get_url(latitude, longitude)
        data = self.request_manager.make_request(
            url=url,
            extend=weather.HOURLY if extend else None, 
            lang=lang, 
            units=units,
            exclude=exclude
        )
        return Forecast(**data)

    def get_time_machine_forecast(
        self, latitude: float, longitude: float, time: datetime, extend: bool=False, 
        lang=languages.ENGLISH, units=units.AUTO, exclude: [weather]=None):
        url = self.get_url(latitude, longitude, int(time.timestamp()))
        data = self.request_manager.make_request(
            url=url,
            extend=weather.HOURLY if extend else None, 
            lang=lang, 
            units=units,
            exclude=exclude
        )
        return Forecast(**data)


class DarkSkyAsync(BaseDarkSky):
    HOST = 'https://api.darksky.net/forecast'

    request_manager_class = RequestMangerAsync

    async def get_forecast(self, 
        latitude: float, longitude: float, extend: bool=None, lang=languages.ENGLISH, 
        units=units.AUTO, exclude: [weather]=None):
        url = self.get_url(latitude, longitude)
        data = await self.request_manager.make_request(
            url=url,
            extend=weather.HOURLY if extend else None, 
            lang=lang, 
            units=units,
            exclude=exclude
        )
        return Forecast(**data)

    async def get_time_machine_forecast(
        self, latitude: float, longitude: float, time: datetime, extend: bool=False, 
        lang=languages.ENGLISH, units=units.AUTO, exclude: [weather]=None):
        url = self.get_url(latitude, longitude, int(time.timestamp()))
        data = await self.request_manager.make_request(
            url=url,
            extend=weather.HOURLY if extend else None, 
            lang=lang, 
            units=units,
            exclude=exclude
        )
        return Forecast(**data)


