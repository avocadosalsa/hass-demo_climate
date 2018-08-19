"""
Demo climate component
"""

import asyncio
import logging

import aiohttp
import async_timeout
import voluptuous as vol

from homeassistant.const import (ATTR_TEMPERATURE, CONF_API_KEY, CONF_ID, TEMP_CELSIUS, TEMP_FAHRENHEIT)
from homeassistant.components.climate import (
    ClimateDevice, ATTR_CURRENT_HUMIDITY, STATE_HEAT, STATE_COOL, STATE_IDLE, STATE_AUTO, PLATFORM_SCHEMA, 
    SUPPORT_TARGET_TEMPERATURE, SUPPORT_TARGET_TEMPERATURE_HIGH, SUPPORT_TARGET_TEMPERATURE_LOW, SUPPORT_TARGET_HUMIDITY, 
    SUPPORT_TARGET_HUMIDITY_HIGH, SUPPORT_TARGET_HUMIDITY_LOW, SUPPORT_FAN_MODE, SUPPORT_OPERATION_MODE, SUPPORT_HOLD_MODE, 
    SUPPORT_SWING_MODE, SUPPORT_AWAY_MODE, SUPPORT_AUX_HEAT, SUPPORT_ON_OFF )
from homeassistant.helpers import config_validation as cv
from homeassistant.helpers.aiohttp_client import async_get_clientsession
from homeassistant.util.temperature import convert as convert_temperature


_LOGGER = logging.getLogger(__name__)

ALL = 'all'
TIMEOUT = 10
FAN_CIRC = "circulate"
FAN_CONT = "continuous"
FAN_AUTO = "auto"

#PLATFORM_SCHEMA = PLATFORM_SCHEMA.extend({
#    vol.Required(CONF_API_KEY): cv.string,
#    vol.Optional(CONF_ID, default=ALL): vol.All(cv.ensure_list, [cv.string]),
#})


@asyncio.coroutine
def async_setup_platform(hass, config, async_add_devices, discovery_info=None):
    """Set up climate devices."""
    devices = []
    devices.append(DemoClimate())

    if devices:
        async_add_devices(devices)


class DemoClimate(ClimateDevice):
    """Representation of a climate device."""

    def __init__(self):
        self._name = "Demo Climate Device"
        self._available = True
        self._humidity = 42
        self._target_humidity = 40
        self._temperature = 24
        self._target_temperature = 23
        self._target_min_temperature = 20
        self._target_max_temperature = 25
        self._temperature_step = 1
        self._operation_modes = {STATE_HEAT, STATE_COOL, STATE_IDLE, STATE_AUTO}
        self._operation_mode = STATE_COOL
        self._fan_modes = {FAN_CIRC, FAN_CONT, FAN_AUTO}
        self._fan_mode = FAN_AUTO
        self._away_mode = False
        self._aux_heat = False
        self._temperature_unit = TEMP_CELSIUS
        self._support_flags = SUPPORT_TARGET_TEMPERATURE | SUPPORT_TARGET_TEMPERATURE_HIGH | SUPPORT_TARGET_TEMPERATURE_LOW | SUPPORT_TARGET_HUMIDITY | SUPPORT_TARGET_HUMIDITY_HIGH | SUPPORT_TARGET_HUMIDITY_LOW | SUPPORT_FAN_MODE | SUPPORT_OPERATION_MODE | SUPPORT_HOLD_MODE | SUPPORT_SWING_MODE | SUPPORT_AWAY_MODE | SUPPORT_AUX_HEAT

    @property
    def supported_features(self):
        """Return the list of supported features."""
        return self._support_flags

    @property
    def name(self):
        """Return the name of the entity."""
        return self._name

    @property
    def available(self):
        """Return True if entity is available."""
        return self._available

    @property
    def temperature_unit(self):
        """Return the unit of measurement which this thermostat uses."""
        return self._temperature_unit

    @property
    def current_humidity(self):
        """Return the current humidity."""
        return self._humidity

    @property
    def target_humidity(self):
        """Return the humidity we try to reach."""
        return self._target_humidity
        
    @property
    def current_operation(self):
        """Return current operation ie. heat, cool, idle."""
        return self._operation_mode
        
    @property
    def operation_list(self):
        """List of available operation modes."""
        return self._operation_modes
        
    @property
    def current_temperature(self):
        """Return the current temperature."""
        return self._temperature
        
    @property
    def target_temperature(self):
        """Return the temperature we try to reach."""
        return self._target_temperature
        
    @property
    def target_temperature_step(self):
        """Return the supported step of target temperature."""
        return self._temperature_step

    @property
    def target_temperature_high(self):
        """Return the highbound target temperature we try to reach."""
        return self._target_max_temperature

    @property
    def target_temperature_low(self):
        """Return the lowbound target temperature we try to reach."""
        return self._target_min_temperature
        
    @property
    def is_away_mode_on(self):
        """Return true if away mode is on."""
        return self._away_mode
        
    @property
    def is_aux_heat_on(self):
        """Return true if AC is on."""
        return self._aux_heat
        
    @property
    def current_fan_mode(self):
        """Return the fan setting."""
        return self._fan_mode

    @property
    def fan_list(self):
        """List of available fan modes."""
        return self._fan_modes


    def set_temperature(self, **kwargs):
        """Set new target temperature."""
        temperature = kwargs.get(ATTR_TEMPERATURE)
        if temperature is None:
            return
            
        temperature = int(temperature)
        if temperature == self._target_temperature:
            return

        self._target_temperature = temperature
        
    def set_humidity(self, humidity):
        """Set new target humidity."""
        if humidity is None:
            return
            
        humidity = int(humidity)
        if humidity == self._target_humidity:
            return
            
        self._target_humidity = humidity

    def set_fan_mode(self, fan):
        """Set new target fan mode."""
        if fan is None:
            return
            
        if fan not in self._fan_modes:
            return
            
        if fan == self._fan_mode:
            return
            
        self._fan_mode = fan

    def set_operation_mode(self, operation_mode):
        """Set new target operation mode."""
        if operation_mode is None:
            return
            
        if operation_mode not in self._operation_modes:
            return
            
        if operation_mode == self._operation_mode:
            return
            
        self._operation_mode = operation_mode

    def turn_away_mode_on(self):
        """Turn away mode on."""
        self._away_mode = True
        
    def turn_away_mode_off(self):
        """Turn away mode off."""
        self._away_mode = False

    def turn_aux_heat_on(self):
        """Turn auxillary heater on."""
        self._aux_heat = True

    def turn_aux_heat_off(self):
        """Turn auxillary heater off."""
        self._aux_heat = False

    def update(self):
        """Retrieve latest state."""
        pass
