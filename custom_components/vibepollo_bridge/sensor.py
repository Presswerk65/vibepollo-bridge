from homeassistant.components.sensor import SensorEntity
from homeassistant.helpers.update_coordinator import CoordinatorEntity
from .const import DOMAIN


async def async_setup_entry(hass, entry, async_add_entities):
    coord = hass.data[DOMAIN][entry.entry_id]

    async_add_entities([
        CurrentGame(coord, entry),
        ActiveConnections(coord, entry),
    ], True)


class Base(CoordinatorEntity):
    def __init__(self, coordinator, entry):
        super().__init__(coordinator)
        self.entry = entry

    @property
    def device_info(self):
        return {
            "identifiers": {(DOMAIN, self.entry.entry_id)},
            "name": "Vibepollo Bridge",
            "manufacturer": "Vibepollo",
            "model": "Streaming Server",
        }


class CurrentGame(Base, SensorEntity):
    def __init__(self, c, entry):
        super().__init__(c, entry)
        self._attr_name = "Current Game"
        self._attr_unique_id = f"{entry.entry_id}_game"

    @property
    def state(self):
        d = self.coordinator.data
        if not d:
            return "none"

        return d.get("session", {}).get("appName") or "none"


class ActiveConnections(Base, SensorEntity):
    def __init__(self, c, entry):
        super().__init__(c, entry)
        self._attr_name = "Active Connections"
        self._attr_unique_id = f"{entry.entry_id}_active_connections"

    @property
    def state(self):
        d = self.coordinator.data
        if not d:
            return 0

        return d.get("session", {}).get("activeSessions", 0)
