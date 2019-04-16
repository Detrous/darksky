import mock
import copy

from .data import DATA


class MockSession(object):
    def __init__(self):
        self.headers = {}
        self.auth = None
        self.mock_json = None

    def get(self, url, params=None):
        return self

    def json(self):
        return copy.deepcopy(DATA)