from homeassistant.components.binary_sensor import BinarySensorEntity
from homeassistant.helpers.update_coordinator import CoordinatorEntity
from .const import DOMAIN


async def async_setup_entry(hass, entry, async_add_entities):
    coordinator = hass.data[DOMAIN][entry.entry_id]

    created = {}

    async def update_entities():
        """Create new client entities dynamically."""
        data = coordinator.data
        if not data:
            return

        clients = data.get("clients", {}).get("named_certs", [])
        new_entities = []

        for cl in clients:
            name = cl.get("name")
            uuid = cl.get("uuid")

            if not name or not uuid:
                continue

            # ✅ UUID als Key (robuster als Name!)
            key = uuid

            if key not in created:
                ent = ClientBinarySensor(coordinator, entry, name, uuid)
                created[key] = ent
                new_entities.append(ent)

        if new_entities:
            async_add_entities(new_entities)

    # ✅ WICHTIG: async listener korrekt registrieren
    coordinator.async_add_listener(
        lambda: hass.async_create_task(update_entities())
    )

    # ✅ initialer Aufbau
    await update_entities()


class ClientBinarySensor(CoordinatorEntity, BinarySensorEntity):
    def __init__(self, coordinator, entry, name, uuid):
        super().__init__(coordinator)

        self.client_name = name
        self.uuid = uuid

        slug = name.lower().replace(" ", "_")

        self._attr_name = f"Client {name}"
        self._attr_unique_id = f"{entry.entry_id}_{slug}"

        self.entry = entry

    @property
    def should_poll(self):
        # ✅ Coordinator steuert Updates
        return False

    @property
    def device_info(self):
        return {
            "identifiers": {(DOMAIN, self.entry.entry_id)},
            "name": "Vibepollo Bridge",
            "manufacturer": "Vibepollo",
            "model": "Streaming Server",
        }

    @property
    def is_on(self):
        """Return True if client is connected."""
        data = self.coordinator.data
        if not data:
            return False

        clients = data.get("clients", {}).get("named_certs", [])

        for cl in clients:
            if cl.get("uuid") == self.uuid:
                return cl.get("connected", False)

        return False

    @property
    def extra_state_attributes(self):
        """Expose additional client details."""
        data = self.coordinator.data
        if not data:
            return {}

        for cl in data.get("clients", {}).get("named_certs", []):
            if cl.get("uuid") == self.uuid:
                return {
                    "last_seen": cl.get("last_seen"),
                    "name": cl.get("name"),
                }

        return {}
