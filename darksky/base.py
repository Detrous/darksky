import pytz
from datetime import datetime

from .utils import undo_snake_case_key, get_datetime_from_unix


class BaseWeather(object):
    summary: str
    icon: str
    data_class: object

    def __init__(self, summary=None, icon=None, data=None, timezone=None):
        self.summary = summary
        self.icon = icon

        assert self.data_class is not None
        self.data = [self.data_class(timezone=timezone, **item) for item in (data or [])]


class AutoInit(object):
    def __init__(self, **params):
        try:
            timezone = pytz.timezone(params.pop('timezone', None))
        except (pytz.UnknownTimeZoneError, AttributeError):
            timezone = pytz.UTC

        fields = [key for key in self.__annotations__]
        for field in fields:
            api_field = undo_snake_case_key(field)
            if self.__annotations__[field] == datetime:
                params[api_field] = get_datetime_from_unix(params.get(api_field), timezone)

            if api_field in params:
                setattr(self, field, params.get(api_field))
            else:
                setattr(self, field, None)