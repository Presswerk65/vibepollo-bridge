
import aiohttp, async_timeout
from datetime import timedelta
from homeassistant.config_entries import ConfigEntry
from homeassistant.helpers.update_coordinator import DataUpdateCoordinator
from .const import DOMAIN

async def async_setup(hass, config):
    return True

async def async_setup_entry(hass, entry: ConfigEntry):
    host=entry.data['host']
    port=entry.data.get('port',47990)
    token=entry.data['token']

    headers={'Authorization':f'Bearer {token}'}
    session=aiohttp.ClientSession(connector=aiohttp.TCPConnector(ssl=False))

    async def update():
        async with async_timeout.timeout(5):
            async with session.get(f"{host}:{port}/api/session/status",headers=headers) as r:
                s=await r.json()
            async with session.get(f"{host}:{port}/api/clients/list",headers=headers) as r:
                c=await r.json()
        return {'session':s,'clients':c}

    coord=DataUpdateCoordinator(hass,None,name='vibepollo',update_method=update,update_interval=timedelta(seconds=5))
    await coord.async_config_entry_first_refresh()

    hass.data.setdefault(DOMAIN,{})
    hass.data[DOMAIN][entry.entry_id]=coord

    await hass.config_entries.async_forward_entry_setups(entry,['sensor','binary_sensor'])
    return True
