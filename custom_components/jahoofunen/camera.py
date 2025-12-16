
import logging
import requests
from datetime import datetime, timedelta
from homeassistant.components.camera import Camera
from .const import DOMAIN

_LOGGER = logging.getLogger(__name__)

SCAN_INTERVAL = timedelta(minutes=15)
API_BASE = "https://jahoo.gr/jfen/api.php"

async def async_setup_entry(hass, config_entry, async_add_entities):
    async_add_entities([JFCartoonCamera()], True)

class JFCartoonCamera(Camera):
    def __init__(self):
        super().__init__()
        self._attr_name = "JF Daily Cartoon EN"
        self._attr_unique_id = "jfen_daily_cartoon_camera"
        self._image_url = None
        self._last_image = None

    def camera_image(self, width=None, height=None):
        if self._image_url:
            try:
                response = requests.get(self._image_url, timeout=10)
                if response.status_code == 200:
                    return response.content
            except Exception as e:
                _LOGGER.error(f"Error fetching camera image: {e}")
        return None

    def update(self):
        try:
            today = datetime.now().strftime('%Y-%m-%d')
            url = f"{API_BASE}?date={today}"
            response = requests.get(url, timeout=10)
            if response.status_code == 200:
                data = response.json()
                if data and 'images' in data and len(data['images']) > 0:
                    self._image_url = data['images'][0]
                else:
                    self._image_url = None
        except Exception as e:
            _LOGGER.error(f"Error updating JF Camera: {e}")
