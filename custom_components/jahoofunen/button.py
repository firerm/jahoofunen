
from homeassistant.components.button import ButtonEntity
from .const import DOMAIN

async def async_setup_entry(hass, config_entry, async_add_entities):
    async_add_entities([
        JFImageButton(hass, "Previous Image", -1, "mdi:arrow-left-bold"),
        JFImageButton(hass, "Next Image", 1, "mdi:arrow-right-bold")
    ], True)

class JFImageButton(ButtonEntity):
    def __init__(self, hass, name, direction, icon):
        self.hass = hass
        self._attr_name = name
        self._attr_unique_id = f"jfen_{'next' if direction > 0 else 'prev'}_button"
        self._direction = direction
        self._attr_icon = icon

    async def async_press(self):
        """Handle the button press."""
        if DOMAIN in self.hass.data and 'camera' in self.hass.data[DOMAIN]:
            camera = self.hass.data[DOMAIN]['camera']
            await camera.change_image(self._direction)
