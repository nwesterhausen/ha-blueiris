"""
Sets up the Blue Iris camera streams
"""
import logging

from homeassistant.const import CONF_NAME, CONF_VERIFY_SSL
from homeassistant.components.camera.mjpeg import (
    CONF_MJPEG_URL, MjpegCamera)
# from homeassistant.components.blue_iris import DOMAIN as BLUEIRIS_DOMAIN

BLUEIRIS_DOMAIN = 'blue_iris'

_LOGGER = logging.getLogger(__name__)

DEPENDENCIES = ['blue_iris']


async def async_setup_platform(hass, config, async_add_entities, discovery_info=None):
    """Set up the Blue Iris cameras"""
    import pyblueiris as bi

    bi_client: bi.BlueIris = hass.data[BLUEIRIS_DOMAIN]
    await bi_client.update_camlist()
    cameras = bi_client.cameras
    if not cameras:
        _LOGGER.warning("No cameras returned from Blue Iris")
        return

    camera_streams = []
    for i in range(len(cameras)):
        cam: bi.BlueIrisCamera = cameras[i]
        _LOGGER.info("Initializing camera {}: {}".format(cam.short_name, cam.display_name))
        await cam.update_camconfig()
        camera_streams.append(BlueIrisCamera(cam))

    async_add_entities(camera_streams)
    return


class BlueIrisCamera(MjpegCamera):
    """Representation of a BlueIris camera stream"""
    from pyblueiris import BlueIrisCamera as bicam

    async def turn_off(self):
        await self.camera.disable()

    async def turn_on(self):
        await self.camera.enable()

    async def enable_motion_detection(self):
        await self.camera.detect_motion(True)

    async def disable_motion_detection(self):
        await self.camera.detect_motion(False)

    def __init__(self, camera: bicam):
        """Initialize subclass of MjpecCamera"""
        device_info = {
            CONF_NAME: camera.display_name,
            CONF_MJPEG_URL: camera.mjpeg_url
        }
        _LOGGER.info("Trying to setup MJPEG for {}, {}".format(camera.display_name, device_info))
        super().__init__(device_info)
        self._is_recording = camera.is_recording
        self._is_available = camera.is_enabled
        self.camera = camera
