import logging

import pi_homeeasy
import voluptuous as vol

from homeassistant.components.switch import PLATFORM_SCHEMA, SwitchEntity
import homeassistant.helpers.config_validation as cv


_LOGGER = logging.getLogger(__name__)

CONF_GPIO_PIN = "gpio_pin"
CONF_EMITTER = "emitter"
CONF_RECEIVER = "receiver"

PLATFORM_SCHEMA = PLATFORM_SCHEMA.extend(
    {
        vol.Optional(CONF_GPIO_PIN, default=17): cv.positive_int,
        vol.Optional(CONF_EMITTER, default=12325262): vol.All(
            vol.Coerce(int), vol.Range(min=1, max=(1 << 26) - 1)
        ),
        vol.Optional(CONF_RECEIVER, default=0): vol.All(
            vol.Coerce(int), vol.Range(min=-1)
        ),
    }
)


def setup_platform(hass, config, add_entities, discovery_info=None):
    _LOGGER.debug("setup_platform(): " + str(config))
    gpio_pin = config.get(CONF_GPIO_PIN)
    emitter = config.get(CONF_EMITTER)
    receiver = config.get(CONF_RECEIVER)
    add_entities([RPiRFHomeEasySwitch(gpio_pin, emitter, receiver)])


class RPiRFHomeEasySwitch(SwitchEntity):
    """Representation of a GPIO RF HomeEasy/Nexa switch."""

    def __init__(self, gpio_pin, emitter, receiver):
        _LOGGER.debug("MySwitch.__init__()")
        self._gpio_pin = gpio_pin
        self._emitter = emitter
        self._receiver = receiver
        self._state = False

    @property
    def device_info(self):
        return {
            "identifiers": {
                # Serial numbers are unique identifiers within a specific domain
                (rpi_rf_homeeasy.DOMAIN, f"{self._gpio_pin}.{self._emitter}")
            },
            "name": self.name,
            CONF_GPIO_PIN: self._gpio_pin,
            CONF_EMITTER: self._emitter,
            CONF_RECEIVER: self._receiver,
        }

    @property
    def should_poll(self):
        """No polling needed."""
        return False

    @property
    def name(self):
        """Return the name of the switch."""
        return "HomeEasy/Nexa"

    @property
    def is_on(self):
        """Return true if device is on."""
        return self._state

    def turn_on(self, **kwargs):
        """Turn the device on."""
        _LOGGER.debug("MySwitch.turn_on()")
        state = True
        pi_homeeasy.send(self._emitter, self._receiver, state, self._gpio_pin)
        self._state = state
        self.schedule_update_ha_state()

    def turn_off(self, **kwargs):
        """Turn the device off."""
        _LOGGER.debug("MySwitch.turn_off()")
        state = False
        pi_homeeasy.send(self._emitter, self._receiver, state, self._gpio_pin)
        self._state = state
        self.schedule_update_ha_state()
