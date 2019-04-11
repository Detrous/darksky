from datetime import datetime


def snake_case_key(key: str) -> str:
    assert isinstance(key, str)
    new_key = key[0]
    for char in key[1:]:
        if char.isupper():
            new_key += '_{char}'.format(char=char.lower())
        else:
            new_key += char
    return new_key