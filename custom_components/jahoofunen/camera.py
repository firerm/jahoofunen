
import logging
import requests
import time
from datetime import datetime, timedelta
from homeassistant.components.camera import Camera
from .const import DOMAIN

_LOGGER = logging.getLogger(__name__)

# Update every 7 minutes to ensure timely day changes
SCAN_INTERVAL = timedelta(minutes=7)
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
        self._last_change = 0
        
        # Register self to hass.data so buttons can find us
        self.hass.data[DOMAIN]['camera'] = self

    @property
    def extra_state_attributes(self):
        """Return attributes to help frontend updates."""
        return {
            "current_image_index": self._index,
            "total_images": len(self._images),
            "last_change_timestamp": self._last_change
        }

    async def change_image(self, direction):
        """Called by button entities to change the image."""
        if not self._images:
            return
        
        self._index = (self._index + direction) % len(self._images)
        self._last_change = time.time()
        # Force HA to refresh the state/image immediately
        self.async_write_ha_state()

    def camera_image(self, width=None, height=None):
        """Return the current image bytes."""
        base_url = FALLBACK_IMAGE
        
        if self._images:
            # Ensure index is within bounds (in case update changed the list size)
            if self._index >= len(self._images):
                self._index = 0
            base_url = self._images[self._index]
        
        # CACHE BUSTING: Append a timestamp query param to the specific image URL
        # This forces the request to bypass any caches (Browser, Cloudflare, HA Proxy)
        separator = "&" if "?" in base_url else "?"
        final_url = f"{base_url}{separator}cache_bust={int(time.time())}"

        try:
            response = requests.get(final_url, timeout=10)
            if response.status_code == 200:
                return response.content
        except Exception as e:
            _LOGGER.error(f"Error fetching camera image: {e}")
            
        return None

    def update(self):
        """Fetch the list of images."""
        try:
            today = datetime.now().strftime('%Y-%m-%d')
            # Add timestamp to prevent caching on the JSON request itself
            url = f"{API_BASE}?date={today}&_t={int(time.time())}"
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
