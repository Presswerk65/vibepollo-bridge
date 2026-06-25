
from homeassistant.components.sensor import SensorEntity
from homeassistant.helpers.update_coordinator import CoordinatorEntity
from .const import DOMAIN

async def async_setup_entry(hass, entry, async_add_entities):
    c=hass.data[DOMAIN][entry.entry_id]
    async_add_entities([Connections(c,entry)],True)

class Connections(CoordinatorEntity,SensorEntity):
    def __init__(self,c,e): super().__init__(c); self._attr_name='Active Connections'; self._attr_unique_id=f"{e.entry_id}_conn"; self.e=e
    @property
    def device_info(self): return {"identifiers":{(DOMAIN,self.e.entry_id)},"name":"Vibepollo Bridge"}
    @property
    def state(self):
        d=self.coordinator.data
        return d['session'].get('activeSessions',0) if d else 0
