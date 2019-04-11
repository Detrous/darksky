DarkSky [![CircleCI](https://circleci.com/gh/Detrous/darksky/tree/master.svg?style=svg)](https://circleci.com/gh/Detrous/darksky/tree/master)
==========

This  library for the [Dark Sky
API](https://darksky.net/dev/docs) provides access to detailed
weather information from around the globe.

* [Installation](#installation)
* [Get started](#get-started)
* [Contact us](#contact-us)
* [License](#license)


### Installation
```
pip3 install darksky_weather
```

### Get started

Before you start using this library, you need to get your API key
[here](https://darksky.net/dev/register).

All classes are fully annotated, source code it's your best doc : )

```python
from darksky.api import DarkSky
from darksky.types import languages, units, weather


API_KEY = '0123456789abcdef9876543210fedcba'

darksky = DarkSky(API_KEY)

latitude = 42.3601
longitude = -71.0589
forecast = darksky.get_forecast(
    latitude, longitude,
    extend=False, # default `False`
    lang=languages.ENGLISH, # default `ENGLISH`
    units=units.AUTO, # default `auto`
    exclude=[weather.MINUTELY, weather.ALERTS] # default `[]`
)

forecast.latitude # 42.3601
forecast.longitude # -71.0589
forecast.timezone # timezone for coordinates. For exmaple: `America/New_York`

forecast.currently # CurrentlyForecast. Can be finded at darksky/forecast.py
forecast.minutely # MinutelyForecast. Can be finded at darksky/forecast.py
forecast.hourly # HourlyForecast. Can be finded at darksky/forecast.py
forecast.daily # DailyForecast. Can be finded at darksky/forecast.py
forecast.alerts # [Alert]. Can be finded at darksky/forecast.py
```

### Contact us.

If you have any issues or questions regarding the library, you are welcome to create an issue, or
You can write an Email to `detrous@protonmail.com`


### License.

Library is released under the [GNU General Public License](./LICENSE).
