import pytz
from datetime import datetime


def undo_snake_case_key(key: str) -> str:
    assert isinstance(key, str)
    new_key = key.split('__')
    int_key = '-'.join(new_key)
    new_key = int_key.split('_')
    return new_key[0] + ''.join([item[0].upper() + item[1:] for item in new_key[1:]])


def get_datetime_from_unix(value: int, timezone: pytz.timezone=pytz.UTC) -> datetime:
    if not isinstance(value, int):
        return
    return datetime.fromtimestamp(value, tz=pytz.UTC).astimezone(timezone)
