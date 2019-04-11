from datetime import datetime


def undo_snake_case_key(key: str) -> str:
    assert isinstance(key, str)
    new_key = key.split('_')
    return new_key[0] + ''.join([item[0].upper() + item[1:] for item in new_key[1:]])


def get_datetime_from_unix(value: int) -> datetime:
    if isinstance(value, int):
        return datetime.fromtimestamp(value)
    return None