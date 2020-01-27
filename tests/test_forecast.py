import asyncio
import copy
import os
import re
import sys
from datetime import datetime

import aioresponses
import mock
import pytest

from darksky.api import DarkSky, DarkSkyAsync
from darksky.forecast import Forecast
from darksky.utils import get_datetime_from_unix

from . import mokcs, utils
from .data import DATA

sys.path.insert(
    0,
    os.path.realpath(
        os.path.join(
            os.path.dirname(__file__),
            ".."
        )
    )
)


@mock.patch("requests.Session", mokcs.MockSession)
def get_forecast_sync() -> Forecast:
    darksky = DarkSky("api_key")

    return darksky.get_forecast(DATA["latitude"], DATA["longitude"])


def get_forecast_async():
    async def get_async_data():
        darksky = DarkSkyAsync("api_key")
        with aioresponses.aioresponses() as resp:
            resp.get(re.compile(".+"), status=200, payload=copy.deepcopy(DATA))

            result = await darksky.get_forecast(
                DATA["latitude"],
                DATA["longitude"]
            )

        # we need to run this manually otherwise we get warnings
        await darksky.request_manager.session.close()
        return result

    loop = asyncio.get_event_loop()
    return loop.run_until_complete(get_async_data())


@pytest.mark.parametrize(
    "forecast",
    [get_forecast_sync(), get_forecast_async()]
)
def test_forecast_base_fields(forecast):

    assert isinstance(forecast, Forecast)
    assert forecast.latitude == DATA["latitude"]
    assert forecast.longitude == DATA["longitude"]
    assert forecast.timezone == "America/New_York"


@pytest.mark.parametrize(
    "forecast",
    [get_forecast_sync(), get_forecast_async()]
)
def test_forecast_currently(forecast):

    f_item, d_item = forecast.currently, copy.deepcopy(DATA["currently"])
    for key in d_item:
        forecast_key = utils.snake_case_key(key)
        if isinstance(getattr(f_item, forecast_key), datetime):
            d_item[key] = get_datetime_from_unix(d_item[key])
        assert hasattr(f_item, forecast_key)
        assert getattr(f_item, forecast_key) == d_item[key]


@pytest.mark.parametrize(
    "forecast",
    [get_forecast_sync(), get_forecast_async()]
)
def test_forecast_minutely(forecast):

    assert forecast.minutely.summary == DATA["minutely"]["summary"]
    assert forecast.minutely.icon == DATA["minutely"]["icon"]

    for f_item, d_item in zip(
        forecast.minutely.data, copy.deepcopy(DATA["minutely"]["data"])
    ):
        for key in d_item:
            forecast_key = utils.snake_case_key(key)
            if isinstance(getattr(f_item, forecast_key), datetime):
                d_item[key] = get_datetime_from_unix(d_item[key])
            assert hasattr(f_item, forecast_key)
            assert getattr(f_item, forecast_key) == d_item[key]


@pytest.mark.parametrize(
    "forecast",
    [get_forecast_sync(), get_forecast_async()]
)
def test_forecast_hourly(forecast):

    assert forecast.hourly.summary == DATA["hourly"]["summary"]
    assert forecast.hourly.icon == DATA["hourly"]["icon"]

    for f_item, d_item in zip(
        forecast.hourly.data, copy.deepcopy(DATA["hourly"]["data"])
    ):
        for key in d_item:
            forecast_key = utils.snake_case_key(key)
            if isinstance(getattr(f_item, forecast_key), datetime):
                d_item[key] = get_datetime_from_unix(d_item[key])
            assert hasattr(f_item, forecast_key)
            assert getattr(f_item, forecast_key) == d_item[key]


@pytest.mark.parametrize(
    "forecast",
    [get_forecast_sync(), get_forecast_async()]
)
def test_forecast_daily(forecast):

    assert forecast.daily.summary == DATA["daily"]["summary"]
    assert forecast.daily.icon == DATA["daily"]["icon"]

    for f_item, d_item in zip(
        forecast.daily.data, copy.deepcopy(DATA["daily"]["data"])
    ):
        for key in d_item:
            forecast_key = utils.snake_case_key(key)
            if isinstance(getattr(f_item, forecast_key), datetime):
                d_item[key] = get_datetime_from_unix(d_item[key])
            assert hasattr(f_item, forecast_key)
            assert getattr(f_item, forecast_key) == d_item[key]


@pytest.mark.parametrize(
    "forecast",
    [get_forecast_sync(), get_forecast_async()]
)
def test_forecast_alerts(forecast):

    for f_item, d_item in zip(forecast.alerts, copy.deepcopy(DATA["alerts"])):
        for key in d_item:
            forecast_key = utils.snake_case_key(key)
            if isinstance(getattr(f_item, forecast_key), datetime):
                d_item[key] = get_datetime_from_unix(d_item[key])
            assert hasattr(f_item, forecast_key)
            assert getattr(f_item, forecast_key) == d_item[key]


@pytest.mark.parametrize(
    "forecast",
    [get_forecast_sync(), get_forecast_async()]
)
def test_forecast_flags(forecast):
    d_item = copy.deepcopy(DATA["flags"])
    f_item = forecast.flags
    for key in d_item:
        forecast_key = utils.snake_case_key(key)
        if isinstance(getattr(f_item, forecast_key), datetime):
            d_item[key] = get_datetime_from_unix(d_item[key])
        assert hasattr(f_item, forecast_key)
        assert getattr(f_item, forecast_key) == d_item[key]
