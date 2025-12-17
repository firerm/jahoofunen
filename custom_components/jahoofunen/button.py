
from homeassistant.components.button import ButtonEntity
from .const import DOMAIN

async def async_setup_entry(hass, config_entry, async_add_entities):
    async_add_entities([
        JFImageButton(hass, "Previous Image", -1, "mdi:arrow-left-bold"),
        JFImageButton(hass, "Next Image", 1, "mdi:arrow-right-bold"),
        JFRefreshButton(hass)
    ], True)

class JFImageButton(ButtonEntity):
    def __init__(self, hass, name, direction, icon):
        self.hass = hass
        self._attr_name = name
        self._attr_unique_id = f"jfen_{'next' if direction > 0 else 'prev'}_button"
        self._direction = direction
        self._attr_icon = icon

    async def async_press(self):
        if DOMAIN in self.hass.data and 'camera' in self.hass.data[DOMAIN]:
            camera = self.hass.data[DOMAIN]['camera']
            await camera.change_image(self._direction)

class JFRefreshButton(ButtonEntity):
    def __init__(self, hass):
        self.hass = hass
        self._attr_name = "Refresh Data"
        self._attr_unique_id = "jfen_refresh_data_button"
        self._attr_icon = "mdi:refresh"

    async def async_press(self):
        """Force update sensor and camera immediately."""
        if DOMAIN in self.hass.data:
            # 1. Update Sensor
            if 'sensor' in self.hass.data[DOMAIN]:
                sensor = self.hass.data[DOMAIN]['sensor']
                await self.hass.async_add_executor_job(sensor.update)
                sensor.async_write_ha_state()
            
            # 2. Update Camera (FETCH JSON)
            if 'camera' in self.hass.data[DOMAIN]:
                camera = self.hass.data[DOMAIN]['camera']
                
                # Increment the hard-refresh counter in the camera
                # This ensures the next image fetch uses a NEW URL signature
                camera.force_refresh_trigger()
                
                # Fetch new JSON list
                await self.hass.async_add_executor_job(camera.update)
                camera.async_write_ha_state()
