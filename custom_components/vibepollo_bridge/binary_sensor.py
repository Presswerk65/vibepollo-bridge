from homeassistant.components.binary_sensor import BinarySensorEntity
from homeassistant.helpers.update_coordinator import CoordinatorEntity
from .const import DOMAIN


async def async_setup_entry(hass, entry, async_add_entities):
    coordinator = hass.data[DOMAIN][entry.entry_id]
    created = {}

    def update():
        data = coordinator.data
        if not data:
            return

        clients = data.get("clients", {}).get("named_certs", [])
        new_entities = []

        for cl in clients:
            name = cl.get("name")
            if not name:
                continue

            key = name.lower().replace(" ", "_")

            if key not in created:
                ent = Client(coordinator, entry, name, key)
                created[key] = ent
                new_entities.append(ent)

        if new_entities:
            async_add_entities(new_entities)

    coordinator.async_add_listener(update)
    update()


class Client(CoordinatorEntity, BinarySensorEntity):
    def __init__(self, coordinator, entry, name, key):
        super().__init__(coordinator)
        self.name = name
        self._attr_name = f"Client {name}"
        self._attr_unique_id = f"{entry.entry_id}_{key}"
        self.entry = entry

    @property
    def device_info(self):
        return {
            "identifiers": {(DOMAIN, self.entry.entry_id)},
            "name": "Vibepollo Bridge",
        }

    @property
    def is_on(self):
        d = self.coordinator.data
        if not d:
            return False

        clients = d.get("clients", {}).get("named_certs", [])

        for c in clients:
            api_name = (c.get("name") or "").strip()
            my_name = (self.name or "").strip()

            if api_name.lower() == my_name.lower():
                return c.get("connected", False)

        return False
