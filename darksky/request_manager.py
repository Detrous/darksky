import aiohttp
import requests

from .exceptions import DarkSkyException


class BaseRequestManger(object):
    def __init__(self, gzip: bool):
        self.headers = {} if not gzip else {"Accept-Encoding": "gzip"}

    def make_request(self, url: str, **params):
        raise NotImplementedError


class RequestManger(BaseRequestManger):
    def __init__(self, gzip: bool):
        super().__init__(gzip)
        self.session = requests.Session()
        self.session.headers = self.headers

    def make_request(self, url: str, **params):
        response = self.session.get(url, params=params).json()
        if "error" in response:
            raise DarkSkyException(response["code"], response["error"])
        response["timezone"] = params.get("timezone") or response["timezone"]
        return response


class RequestMangerAsync(BaseRequestManger):
    def __init__(self, gzip: bool, client_session: aiohttp.ClientSession = None):
        super().__init__(gzip)
        assert (
            isinstance(client_session, aiohttp.ClientSession) or client_session is None
        )
        self.session = (
            aiohttp.ClientSession() if client_session is None else client_session
        )

    async def make_request(self, url: str, **params):
        # Fix for yarl(Doesn't support any types besides str)
        for key in params.copy():
            if params[key] is None:
                del params[key]

        async with self.session.get(url, params=params, headers=self.headers) as resp:
            response = await resp.json()
            if "error" in response:
                raise DarkSkyException(response["code"], response["error"])
        response["timezone"] = params.get("timezone") or response["timezone"]
        return response
