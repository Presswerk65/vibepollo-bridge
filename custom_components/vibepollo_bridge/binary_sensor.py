
from homeassistant.components.binary_sensor import BinarySensorEntity
from homeassistant.helpers.update_coordinator import CoordinatorEntity
from .const import DOMAIN

async def async_setup_entry(hass, entry, async_add_entities):
    c=hass.data[DOMAIN][entry.entry_id]
    created={}

    def update():
        data=c.data
        if not data: return
        clients=data.get('clients',{}).get('named_certs',[])
        new=[]
        for cl in clients:
            name=cl.get('name')
            key=name.lower().replace(' ','_')
            if key not in created:
                ent=Client(c,entry,name,key)
                created[key]=ent
                new.append(ent)
        if new: async_add_entities(new)

    c.async_add_listener(update)
    update()

class Client(CoordinatorEntity,BinarySensorEntity):
    def __init__(self,c,e,name,key):
        super().__init__(c)
        self.name=name
        self._attr_name=f"Client {name}"
        self._attr_unique_id=f"{e.entry_id}_{key}"
        self.e=e
    @property
    def device_info(self): return {"identifiers":{(DOMAIN,self.e.entry_id)}}
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
