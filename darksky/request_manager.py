import requests
import aiohttp
from .exceptions import DarkSkyException


class BaseRequestManger(object):
    def __init__(self, gzip: bool):
        self.headers = {} if not gzip else {'Accept-Encoding': 'gzip'}

    def make_request(self, url: str, **params):
        raise NotImplementedError


class RequestManger(BaseRequestManger):
    def __init__(self, gzip: bool):
        super().__init__(gzip)
        self.session = requests.Session()
        self.session.headers = self.headers

    def make_request(self, url: str, **params):
        response = self.session.get(url, params=params).json()
        if 'error' in response:
            raise DarkSkyException(response['code'], response['error'])
        return response


class RequestMangerAsync(BaseRequestManger):
    async def make_request(self, url: str, **params):
        # Fix for yarl(Doesn't support any types besides str)
        for key in params.copy():
            if params[key] is None:
                del params[key]
            
        async with aiohttp.ClientSession().get(url, params=params, headers=self.headers) as resp:
            response = await resp.json()
            if 'error' in response:
                raise DarkSkyException(response['code'], response['error'])
        return response