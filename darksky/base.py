from datetime import datetime

import pytz

from .utils import get_datetime_from_unix, undo_snake_case_key


class BaseWeather:
    summary: str
    icon: str
    data_class: object

    def __init__(self, summary=None, icon=None, data=None, timezone=None):
        self.summary = summary
        self.icon = icon

        assert self.data_class is not None
        self.data = [self.data_class(timezone=timezone, **item)
                     for item in (data or [])]

    def __repr__(self):
        return '%s([%d])' % (self.__class__.__name__, len(self.data))

    def __iter__(self):
        return iter(self.data)


class AutoInit:

    def __init__(self, **params):
        try:
            timezone = pytz.timezone(params.pop('timezone', None))
        except (pytz.UnknownTimeZoneError, AttributeError):
            timezone = pytz.UTC

        for field in self.__annotations__:
            api_field = undo_snake_case_key(field)
            if self.__annotations__[field] == datetime:
                params[api_field] = get_datetime_from_unix(
                    params.get(api_field),
                    timezone
                )

            if api_field in params:
                setattr(self, field, params.get(api_field))
            else:
                setattr(self, field, None)

    def __iter__(self):
        return iter(self.__dict__.items())

    def __repr__(self):
        return '%s(%s)' % (self.__class__.__name__, getattr(self, 'time', ''))
