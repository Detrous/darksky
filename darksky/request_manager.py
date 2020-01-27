import requests
from aiohttp import ClientSession

from .exceptions import DarkSkyException


class BaseRequestManger:
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
    def __init__(self, gzip: bool, client_session: ClientSession = None):
        super().__init__(gzip)
        assert (
            isinstance(client_session, ClientSession) or client_session is None
        )
        self.session = (
            ClientSession() if client_session is None else client_session
        )

    async def make_request(self, url: str, **params):

        for key in list(params.keys()):
            if params[key] is None:
                del params[key]
            elif isinstance(params[key], list):
                params[key] = ','.join(params[key])

        async with self.session.get(
            url,
            params=params,
            headers=self.headers
        ) as resp:
            response = await resp.json()
            if "error" in response:
                raise DarkSkyException(response["code"], response["error"])
        response["timezone"] = params.get("timezone") or response["timezone"]
        return response
