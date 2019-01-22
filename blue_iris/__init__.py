"""
Component for connecting Home Assistant to a Blue Iris server.
"""
import voluptuous as vol

from homeassistant.helpers import aiohttp_client, config_validation as cv
from homeassistant.const import (
    CONF_NAME, CONF_HOST, CONF_PORT, CONF_USERNAME, CONF_PASSWORD
)
import logging

DOMAIN = 'blue_iris'
_LOGGER = logging.getLogger(__name__)

CONF_PROTOCOL = 'protocol'
REQUIREMENTS = ['pyblueiris==0.2.8']

DEFAULT_PROTOCOL = "http"
DEFAULT_PORT = 1  # This is set as the default, a 1 is changed to 80 for http and 443 for https
DEFAULT_NAME = "server"

ENTITY_ID_FORMAT = 'blue_iris.{}'

STATE_CONNECTED = 'Connected'
STATE_DISCONNECTED = 'Disconnected'

ATTR_NAME = "Server name"
ATTR_VERSION = "Blue Iris Version"
ATTR_NUM_CAMERAS = "Number of Cameras"
ATTR_ADMIN = "Authenticated as Admin"
ATTR_PROFILES = "Available Profiles"
ATTR_SCHEDULES = "Available Schedules"
ATTR_API_URL = "JSON API Endpoint"

# The config that zone accepts is the same as if it has platforms.
CONFIG_SCHEMA = vol.Schema({
    DOMAIN: vol.Schema({vol.Required(CONF_USERNAME): cv.string,
                        vol.Required(CONF_PASSWORD): cv.string,
                        vol.Required(CONF_HOST): cv.string,
                        vol.Optional(CONF_PROTOCOL, default=DEFAULT_PROTOCOL): cv.string,
                        vol.Optional(CONF_PORT, default=DEFAULT_PORT): cv.port,
                        vol.Optional(CONF_NAME, default=DEFAULT_NAME): cv.string
                        })
}, extra=vol.ALLOW_EXTRA)


async def async_setup(hass, config):
    """Set up component from configuration.yaml"""
    from pyblueiris import BlueIris as bi

    _LOGGER.info("Starting setup of Blue Iris")
    conf = config.get(DOMAIN)
    _LOGGER.info(conf)

    if conf is None:
        return True
    port = conf.get(CONF_PORT)
    if port is 1:
        if conf.get(CONF_PROTOCOL) == 'http':
            port = 80
        else:
            port = 443

    websession = aiohttp_client.async_get_clientsession(hass)

    hass.data[DOMAIN] = blue = bi(websession,
                                  conf.get(CONF_USERNAME),
                                  conf.get(CONF_PASSWORD),
                                  conf.get(CONF_PROTOCOL),
                                  conf.get(CONF_HOST),
                                  port,
                                  debug=True,
                                  logger=_LOGGER)

    login_successful = await hass.data[DOMAIN].setup_session()
    if not login_successful:
        _LOGGER.error("Failed to login to server")
        return False
    _LOGGER.info("Connected to {} running Blue Iris v.{}".format(hass.data[DOMAIN].name,
                                                                 hass.data[DOMAIN].version))
    await blue.update_all_information()
    hass.states.async_set(entity_id=ENTITY_ID_FORMAT.format(blue.name),
                                new_state=STATE_CONNECTED,
                                attributes={ATTR_ADMIN: blue.admin,
                                            ATTR_NAME: blue.name,
                                            ATTR_PROFILES: blue.attributes["profiles"],
                                            ATTR_SCHEDULES: blue.attributes["schedules"],
                                            ATTR_VERSION: blue.version,
                                            ATTR_NUM_CAMERAS: len(blue.cameras),
                                            ATTR_API_URL: blue.url}
                                )
    return True
