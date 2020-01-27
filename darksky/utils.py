from datetime import datetime

from pytz import UTC, timezone


def undo_snake_case_key(key: str) -> str:
    assert isinstance(key, str)
    new_key = key.split('__')
    int_key = '-'.join(new_key)
    new_key = int_key.split('_')
    return new_key[0] + ''.join([it.title() for it in new_key[1:]])


def get_datetime_from_unix(value: int, tz: timezone = UTC) -> datetime:
    if not isinstance(value, int):
        return None
    return datetime.fromtimestamp(value, tz=UTC).astimezone(tz)
