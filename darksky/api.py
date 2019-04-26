import requests
from datetime import datetime

from .forecast import Forecast
from .types import languages, units, weather


class DarkSky(object):
    HOST = 'https://api.darksky.net/forecast'

    def __init__(self, api_key, gzip: bool=True):
        self.api_key = api_key

        self.__request_manager = RequestManger(gzip)

    def get_forecast(self, 
        latitude: float, longitude: float, extend: bool=None, lang=languages.ENGLISH, 
        units=units.AUTO, exclude: [weather]=None):
        return self.__get_forecast(
            latitude, longitude, 
            extend=weather.HOURLY if extend else None, 
            lang=lang, 
            units=units,
            exclude=exclude
        )

    def get_time_machine_forecast(
        self, latitude: float, longitude: float, time: datetime, extend: bool=False, 
        lang=languages.ENGLISH, units=units.AUTO, exclude: [weather]=None):
        return self.__get_forecast(
            latitude, longitude, int(time.timestamp()),
            extend=weather.HOURLY if extend else None, 
            lang=lang, 
            units=units,
            exclude=exclude
        )

    def __get_forecast(self, latitude: float, longitude: float, time=None, **params):
        if time is None:
            url = '{host}/{api_key}/{latitude},{longitude}'.format(
                api_key=self.api_key,
                host=self.HOST,
                latitude=latitude,
                longitude=longitude
            )
        else: 
            url = '{host}/{api_key}/{latitude},{longitude},{time}'.format(
                api_key=self.api_key,
                host=self.HOST,
                latitude=latitude,
                longitude=longitude,
                time=time
            )
        data = self.__request_manager.make_request(url, **params)
        return Forecast(**data)


class RequestManger(object):
    def __init__(self, gzip: bool):
        self.session = requests.Session()
        if gzip:
            self.session.headers['Accept-Encoding'] = 'gzip'

    def make_request(self, url: str, **params):
        return self.session.get(url, params=params).json()
