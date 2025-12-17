
import logging
import requests
import time
import uuid
from datetime import datetime, timedelta
from homeassistant.components.camera import Camera
from .const import DOMAIN

_LOGGER = logging.getLogger(__name__)

# Update list of images every 15 minutes (manual refresh available)
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
        self._last_change = 0
        
        # This counter increases every time Refresh is pressed
        # It is appended to the URL to force a hard reload
        self._force_update_counter = 0
        
        # Register self to hass.data so buttons can find us
        if DOMAIN not in self.hass.data:
            self.hass.data[DOMAIN] = {}
        self.hass.data[DOMAIN]['camera'] = self

    @property
    def extra_state_attributes(self):
        """Return attributes to help frontend updates."""
        return {
            "current_image_index": self._index,
            "total_images": len(self._images),
            "last_change_timestamp": self._last_change,
            "force_update_counter": self._force_update_counter
        }

    async def change_image(self, direction):
        """Called by button entities to change the image index."""
        if not self._images:
            return
        
        self._index = (self._index + direction) % len(self._images)
        self._last_change = time.time()
        self.async_write_ha_state()

    def force_refresh_trigger(self):
        """Called by the Refresh button to increment counter."""
        self._force_update_counter += 1
        # Also reset index just in case
        if self._images:
            if self._index >= len(self._images):
                self._index = 0
        self.async_write_ha_state()

    def camera_image(self, width=None, height=None):
        """Return the current image bytes."""
        base_url = FALLBACK_IMAGE
        
        if self._images:
            # Ensure index is within bounds
            if self._index >= len(self._images):
                self._index = 0
            base_url = self._images[self._index]
        
        # AGGRESSIVE CACHE BUSTING STRATEGY
        # 1. Use the force_update_counter from the button
        # 2. Use a random UUID for every fetch to bypass local caches
        random_id = str(uuid.uuid4())
        separator = "&" if "?" in base_url else "?"
        
        # We include the 'v' parameter which tracks the button presses
        final_url = f"{base_url}{separator}_rand={random_id}&v={self._force_update_counter}"

        try:
            headers = {
                "Cache-Control": "no-cache, no-store, must-revalidate",
                "Pragma": "no-cache",
                "Expires": "0",
                "User-Agent": f"Home Assistant/JFEN-Integration-v0.1.4-{self._force_update_counter}"
            }
            
            response = requests.get(final_url, headers=headers, timeout=15)
            if response.status_code == 200:
                return response.content
        except Exception as e:
            _LOGGER.error(f"Error fetching camera image: {e}")
            
        return None

    def update(self):
        """Fetch the list of images."""
        try:
            today = datetime.now().strftime('%Y-%m-%d')
            # Cache bust the API JSON call
            url = f"{API_BASE}?date={today}&_t={int(time.time())}&v={self._force_update_counter}"
            
            headers = {
                "Cache-Control": "no-cache, no-store, must-revalidate",
                "Pragma": "no-cache",
                "Expires": "0"
            }
            
            response = requests.get(url, headers=headers, timeout=10)
            if response.status_code == 200:
                data = response.json()
                if data and 'images' in data and len(data['images']) > 0:
                    self._images = data['images']
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
