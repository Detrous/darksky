import os, sys
sys.path.insert(0, os.path.realpath(os.path.join(os.path.dirname(__file__), '..')))

import mock
import pytest
from datetime import datetime

from darksky.api import DarkSky
from darksky.forecast import Forecast
from darksky.utils import get_datetime_from_unix

from .data import DATA
from . import mokcs, utils


@mock.patch('requests.Session', mokcs.MockSession)
def get_forecast() -> Forecast:
    darksky = DarkSky('api_key')

    return darksky.get_forecast(DATA['latitude'], DATA['longitude'])


def test_forecast_base_fields():
    forecast = get_forecast()

    assert forecast.latitude == DATA['latitude']
    assert forecast.longitude == DATA['longitude']
    assert forecast.timezone == 'America/New_York'


def test_forecast_currently():
    forecast = get_forecast()

    forecast_item, data_item = forecast.currently, DATA['currently']
    for key in data_item:
        forecast_key = utils.snake_case_key(key)
        if isinstance(getattr(forecast_item, forecast_key), datetime):
            data_item[key] = get_datetime_from_unix(data_item[key])
        assert hasattr(forecast_item, forecast_key)
        assert getattr(forecast_item, forecast_key) == data_item[key]


def test_forecast_minutely():
    forecast = get_forecast()

    assert forecast.minutely.summary == DATA['minutely']['summary']
    assert forecast.minutely.icon == DATA['minutely']['icon']

    for forecast_item, data_item in zip(forecast.minutely.data, DATA['minutely']['data']):
        for key in data_item:
            forecast_key = utils.snake_case_key(key)
            if isinstance(getattr(forecast_item, forecast_key), datetime):
                data_item[key] = get_datetime_from_unix(data_item[key]) 
            assert hasattr(forecast_item, forecast_key)
            assert getattr(forecast_item, forecast_key) == data_item[key]
    

def test_forecast_hourly():
    forecast = get_forecast()

    assert forecast.hourly.summary == DATA['hourly']['summary']
    assert forecast.hourly.icon == DATA['hourly']['icon']

    for forecast_item, data_item in zip(forecast.hourly.data, DATA['hourly']['data']):
        for key in data_item:
            forecast_key = utils.snake_case_key(key)
            if isinstance(getattr(forecast_item, forecast_key), datetime):
                data_item[key] = get_datetime_from_unix(data_item[key])
            assert hasattr(forecast_item, forecast_key)
            assert getattr(forecast_item, forecast_key) == data_item[key]


def test_forecast_daily():
    forecast = get_forecast()

    assert forecast.daily.summary == DATA['daily']['summary']
    assert forecast.daily.icon == DATA['daily']['icon']

    for forecast_item, data_item in zip(forecast.daily.data, DATA['daily']['data']):
        for key in data_item:
            forecast_key = utils.snake_case_key(key)
            if isinstance(getattr(forecast_item, forecast_key), datetime):
                data_item[key] = get_datetime_from_unix(data_item[key])
            assert hasattr(forecast_item, forecast_key)
            assert getattr(forecast_item, forecast_key) == data_item[key]


def test_forecast_alerts():
    forecast = get_forecast()

    for forecast_item, data_item in zip(forecast.alerts, DATA['alerts']):
        for key in data_item:
            forecast_key = utils.snake_case_key(key)
            if isinstance(getattr(forecast_item, forecast_key), datetime):
                data_item[key] = get_datetime_from_unix(data_item[key])
            assert hasattr(forecast_item, forecast_key)
            assert getattr(forecast_item, forecast_key) == data_item[key]

