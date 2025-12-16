
import logging
import requests
from datetime import datetime, timedelta
from homeassistant.components.camera import Camera
from .const import DOMAIN

_LOGGER = logging.getLogger(__name__)

SCAN_INTERVAL = timedelta(minutes=15)
API_BASE = "https://jahoo.gr/jfen/api.php"
FALLBACK_IMAGE = "https://jahoo.gr/jfen/logos/photonotfound.png"

async def async_setup_entry(hass, config_entry, async_add_entities):
    cam = JFCartoonCamera(hass)
    async_add_entities([cam], True)

class JFCartoonCamera(Camera):
    def __init__(self, hass):
        super().__init__()
        self.hass = hass
        self._attr_name = "JFEN Daily Cartoon"
        self._attr_unique_id = "jfen_daily_cartoon_camera"
        self._images = []
        self._index = 0
        
        # Register self to hass.data so buttons can find us
        self.hass.data[DOMAIN]['camera'] = self

    @property
    def extra_state_attributes(self):
        """Return attributes to help frontend updates."""
        return {
            "current_image_index": self._index,
            "total_images": len(self._images),
            "image_source_url": self._images[self._index] if self._images and self._index < len(self._images) else "None"
        }

    async def change_image(self, direction):
        """Called by button entities to change the image."""
        if not self._images:
            return
        
        self._index = (self._index + direction) % len(self._images)
        # Force HA to refresh the state/image immediately
        self.async_write_ha_state()

    def camera_image(self, width=None, height=None):
        """Return the current image bytes."""
        current_url = FALLBACK_IMAGE
        
        if self._images:
            # Ensure index is within bounds (in case update changed the list size)
            if self._index >= len(self._images):
                self._index = 0
            current_url = self._images[self._index]
        
        try:
            response = requests.get(current_url, timeout=10)
            if response.status_code == 200:
                return response.content
        except Exception as e:
            _LOGGER.error(f"Error fetching camera image: {e}")
            
        return None

    def update(self):
        """Fetch the list of images."""
        try:
            today = datetime.now().strftime('%Y-%m-%d')
            url = f"{API_BASE}?date={today}"
            response = requests.get(url, timeout=10)
            if response.status_code == 200:
                data = response.json()
                if data and 'images' in data and len(data['images']) > 0:
                    self._images = data['images']
                    # Keep index within bounds if list shrank
                    if self._index >= len(self._images):
                        self._index = 0
                else:
                    self._images = []
                    self._index = 0
            else:
                self._images = []
        except Exception as e:
            _LOGGER.error(f"Error updating JF Camera: {e}")
            self._images = []
