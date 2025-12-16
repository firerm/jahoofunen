
import logging
import requests
from datetime import datetime, timedelta
from homeassistant.components.sensor import SensorEntity
from .const import DOMAIN

_LOGGER = logging.getLogger(__name__)

# Update every 7 minutes to ensure timely day changes
SCAN_INTERVAL = timedelta(minutes=7)
API_BASE = "https://jahoo.gr/jfen/api.php"
VIEWER_BASE_URL = "https://jahoo.gr/jfen/?mode=viewer"

async def async_setup_entry(hass, config_entry, async_add_entities):
    async_add_entities([JFCartoonSensor()], True)

class JFCartoonSensor(SensorEntity):
    def __init__(self):
        self._attr_name = "JFEN Daily Cartoon"
        self._attr_unique_id = "jfen_daily_cartoon_sensor"
        self._attr_native_value = "Initializing"
        self._attr_extra_state_attributes = {}

    @property
    def icon(self):
        return "mdi:emoticon-happy-outline"

    def update(self):
        try:
            today = datetime.now().strftime('%Y-%m-%d')
            url = f"{API_BASE}?date={today}"
            response = requests.get(url, timeout=10)
            if response.status_code == 200:
                data = response.json()
                if data and 'title' in data:
                    self._attr_native_value = data['title']
                    viewer_url = f"{VIEWER_BASE_URL}&date={data.get('date', '')}"
                    images = data.get('images', [])
                    self._attr_extra_state_attributes = {
                        "description": data.get('description', ''),
                        "images_count": len(images),
                        "date": data.get('date', ''),
                        "viewer_url": viewer_url
                    }
                else:
                    self._attr_native_value = "No Cartoon Today"
                    self._attr_extra_state_attributes = {
                        "viewer_url": VIEWER_BASE_URL
                    }
        except Exception as e:
            _LOGGER.error(f"Error updating JF Sensor: {e}")
