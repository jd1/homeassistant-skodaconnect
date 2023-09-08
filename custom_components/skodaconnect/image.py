"""
Support for Skoda Connect.
"""
import logging

from homeassistant.components.image import ImageEntity
from homeassistant.const import CONF_RESOURCES

from . import DATA, DATA_KEY, DOMAIN, SkodaEntity

_LOGGER = logging.getLogger(__name__)

async def async_setup_platform(hass, config, async_add_entities, discovery_info=None):
    """ Setup the Skoda switch."""
    if discovery_info is None:
        return
    async_add_entities([SkodaImage(hass.data[DATA_KEY], *discovery_info)])


async def async_setup_entry(hass, entry, async_add_devices):
    data = hass.data[DOMAIN][entry.entry_id][DATA]
    coordinator = data.coordinator
    if coordinator.data is not None:
        if CONF_RESOURCES in entry.options:
            resources = entry.options[CONF_RESOURCES]
        else:
            resources = entry.data[CONF_RESOURCES]

        async_add_devices(
            SkodaImage(
                data, instrument.vehicle_name, instrument.component, instrument.attr
            )
            for instrument in (
                instrument
                for instrument in data.instruments
                if instrument.component == "image" and instrument.attr in resources
            )
        )

    return True


class SkodaImage(SkodaEntity, ImageEntity):
    """Representation of a Skoda Image """

    @property
    def image_url(self):
        return self.instrument.state
