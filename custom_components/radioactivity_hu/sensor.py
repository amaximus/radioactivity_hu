import asyncio
import json
import logging
import voluptuous as vol
import aiohttp
from datetime import timedelta
from datetime import datetime

from homeassistant.components.sensor import PLATFORM_SCHEMA
from homeassistant.helpers.aiohttp_client import async_get_clientsession
import homeassistant.helpers.config_validation as cv
from homeassistant.helpers.entity import Entity
from homeassistant.helpers.discovery import async_load_platform

REQUIREMENTS = [ ]

_LOGGER = logging.getLogger(__name__)

CONF_ATTRIBUTION = "Data provided by katasztrofavedelem.hu"
CONF_NAME = 'name'
CONF_STATION = 'station'

DEFAULT_NAME = 'Radioactivity HU'
DEFAULT_STATION = ''
DEFAULT_ICON = 'mdi:radioactive'

SCAN_INTERVAL = timedelta(minutes=30)
TWO_DAYS = 172800 # secs

PLATFORM_SCHEMA = PLATFORM_SCHEMA.extend({
    vol.Optional(CONF_NAME, default=DEFAULT_NAME): cv.string,
    vol.Optional(CONF_STATION, default=DEFAULT_STATION): cv.string,
})

@asyncio.coroutine
def async_setup_platform(hass, config, async_add_devices, discovery_info=None):
    name = config.get(CONF_NAME)
    station = config.get(CONF_STATION)

    async_add_devices(
        [RadioactivityHUSensor(hass, name, station )],update_before_add=True)

async def async_get_wqdata(self):
    wqjson = {}
    url = 'https://www.katasztrofavedelem.hu/application/uploads/cache/hattersugarzas/RAD.json'
    async with self._session.get(url) as response:
        rsp1 = await response.text()

    wqjson = json.loads(rsp1)

    return wqjson

class RadioactivityHUSensor(Entity):

    def __init__(self, hass, name, station):
        """Initialize the sensor."""
        self._hass = hass
        self._name = name
        self._station = station
        self._state = None
        self._wqdata = {}
        self._icon = DEFAULT_ICON
        self._session = async_get_clientsession(hass)
        self._attr = {}

    @property
    def extra_state_attributes(self):

        return self._attr

    @asyncio.coroutine
    async def async_update(self):
        wqdata = await async_get_wqdata(self)
        max_state = 0
        max_station = ''
        max_lasttime = ''

        self._attr["provider"] = CONF_ATTRIBUTION
        self._attr["unit_of_measurement"] = "nSv/h"

        if 'errorMessage' in wqdata and wqdata["errorMessage"] == "OK":
            self._wqdata = wqdata

            today = datetime.now()

            for i in wqdata["data"]:
                if len(self._station) != 0:
                    if i["location"] == self._station:
                        self._state = str(int(float(i["lastMeasurement"])))
                        self._attr["last_measurement_time"] = i["lastMeasurementTime"]
                        self._attr["station"] = self._station
                        self._attr["active"] = i["active"]
                        break
                else:
                   if i["lastMeasurement"] == None or i["active"] == None:
                       continue
                   if i["active"] == "false":
                       continue

                   if i["lastMeasurementTime"] != None:
                       tstamp = datetime.strptime(i["lastMeasurementTime"],"%Y-%m-%d %H:%M:%S").date()
                       if int(datetime.now().strftime('%s')) - int(tstamp.strftime('%s')) > TWO_DAYS:
                           continue

                   if float(i["lastMeasurement"]) > max_state:
                       max_state = float(i["lastMeasurement"])
                       max_station = i["location"]
                       max_lasttime = i["lastMeasurementTime"]
            if len(self._station) == 0:
                self._state = str(int(max_state))
                self._attr["station"] = max_station
                self._attr["last_measurement_time"] = max_lasttime
                self._attr["active"] = "true"

        _LOGGER.debug(self._state)
        _LOGGER.debug(self._attr)
        return self._state

    @property
    def name(self):
        return self._name

    @property
    def state(self):
        return self._state

    @property
    def icon(self):
        return DEFAULT_ICON
