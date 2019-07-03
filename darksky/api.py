import requests
from datetime import datetime

from .forecast import Forecast
from .exceptions import DarkSkyException
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
            exclude=exclude,
            func=self.get_forecast
        )

    def get_time_machine_forecast(
        self, latitude: float, longitude: float, time: datetime, extend: bool=False, 
        lang=languages.ENGLISH, units=units.AUTO, exclude: [weather]=None):
        return self.__get_forecast(
            latitude, longitude, int(time.timestamp()),
            extend=weather.HOURLY if extend else None, 
            lang=lang, 
            units=units,
            exclude=exclude,
            func=self.get_time_machine_forecast
        )

    def __get_forecast(self, latitude: float, longitude: float, time=None, **params):
        refresh_func = params.pop('func')
        refresh_kwargs = {
            **{'latitude': latitude, 'longitude': longitude},
            **params
        }

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
            refresh_kwargs['time'] = time

        data = self.__request_manager.make_request(url, **params)
        return Forecast(**data, refresh_data={
            'func': refresh_func,
            'kwargs': refresh_kwargs
        })


class RequestManger(object):
    def __init__(self, gzip: bool):
        self.session = requests.Session()
        if gzip:
            self.session.headers['Accept-Encoding'] = 'gzip'

    def make_request(self, url: str, **params):
        response = self.session.get(url, params=params).json()
        if 'error' in response:
            raise DarkSkyException(response['code'], response['error'])
        return response