import os
import sys
from typing import List

import pytest

from darksky.base import AutoInit, BaseWeather
from darksky.utils import undo_snake_case_key

sys.path.insert(0, os.path.realpath(os.path.join(os.path.dirname(__file__), "..")))




def test_undo_snake_case_key():
    undo_key = undo_snake_case_key("snake_key")
    assert undo_key == "snakeKey"


def test_undo_snake_case_key_one_item():
    undo_key = undo_snake_case_key("key")
    assert undo_key == "key"


def test_undo_snake_case_key_bad_value_type():
    with pytest.raises(AssertionError):
        undo_snake_case_key(1)


def test_base_weather():
    class TestDataBaseWeather(object):
        def __init__(self, test_field, **kwargs):
            self.test_field = test_field

    class TestBaseWeather(BaseWeather):
        data: List[TestDataBaseWeather]
        data_class = TestDataBaseWeather

    test_base_weather_obj = TestBaseWeather(
        "summary", "icon", data=[{"test_field": "data"}]
    )

    assert test_base_weather_obj.summary == "summary"
    assert test_base_weather_obj.icon == "icon"
    assert test_base_weather_obj.data[0].test_field == "data"


def test_auto_init():
    class TestAutoInit(AutoInit):
        field: str

    test_auto_init_obj = TestAutoInit(field="data")
    assert test_auto_init_obj.field == "data"


def test_auto_init__field_exists_on_class_but_is_not_given_in_constructor__defaults_to_none():
    class TestAutoInit(AutoInit):
        field: str
        other_field: int

    test_auto_init_obj = TestAutoInit(field="data")
    assert test_auto_init_obj.field == "data"
    assert test_auto_init_obj.other_field == None
