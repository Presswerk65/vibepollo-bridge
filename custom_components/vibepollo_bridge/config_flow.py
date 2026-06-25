
import voluptuous as vol
from homeassistant import config_entries
import aiohttp

DOMAIN="vibepollo_bridge"

class ConfigFlow(config_entries.ConfigFlow,domain=DOMAIN):
    VERSION=1

    async def async_step_user(self,user_input=None):
        errors={}

        if user_input:
            host=user_input['host']
            token=user_input['token']
            port=user_input.get('port',47990)

            if not host.startswith('http'):
                host=f"https://{host}"

            try:
                async with aiohttp.ClientSession(connector=aiohttp.TCPConnector(ssl=False)) as s:
                    async with s.get(f"{host}:{port}/api/session/status",headers={'Authorization':f'Bearer {token}'}) as r:
                        if r.status!=200:
                            errors['base']='cannot_connect'

                if not errors:
                    return self.async_create_entry(title=host,data={'host':host,'port':port,'token':token})
            except:
                errors['base']='cannot_connect'

        return self.async_show_form(step_id='user',data_schema=vol.Schema({
            vol.Required('host'):str,
            vol.Required('token'):str
        }),errors=errors)
