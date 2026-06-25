import logging
from datetime import timedelta

import aiohttp
import async_timeout

from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant
from homeassistant.helpers.update_coordinator import DataUpdateCoordinator

from .const import DOMAIN

_LOGGER = logging.getLogger(__name__)


async def async_setup(hass: HomeAssistant, config: dict):
    """Set up integration (YAML not used)."""
    return True


async def async_setup_entry(hass: HomeAssistant, entry: ConfigEntry):
    """Set up Vibepollo Bridge from a config entry."""

    host = entry.data["host"]
    port = entry.data.get("port", 47990)
    token = entry.data["token"]

    headers = {"Authorization": f"Bearer {token}"}

    # ✅ SSL ignore (self-signed support)
    session = aiohttp.ClientSession(
        connector=aiohttp.TCPConnector(ssl=False)
    )

    async def async_update_data():
        """Fetch data from Vibepollo API."""
        try:
            async with async_timeout.timeout(5):

                # 🔹 Session Status
                async with session.get(
                    f"{host}:{port}/api/session/status",
                    headers=headers,
                ) as resp:
                    if resp.status != 200:
                        raise Exception(f"Session API error: {resp.status}")
                    session_data = await resp.json()

                # 🔹 Clients
                async with session.get(
                    f"{host}:{port}/api/clients/list",
                    headers=headers,
                ) as resp:
                    if resp.status != 200:
                        raise Exception(f"Clients API error: {resp.status}")
                    clients_data = await resp.json()

                return {
                    "session": session_data,
                    "clients": clients_data,
                }

        except Exception as err:
            _LOGGER.error("Vibepollo update failed: %s", err)
            return None

    # ✅ FIX: logger MUST NOT be None
    coordinator = DataUpdateCoordinator(
        hass,
        _LOGGER,  # ✅ critical FIX
        name="vibepollo_bridge",
        update_method=async_update_data,
        update_interval=timedelta(seconds=5),
    )

    # first refresh (required!)
    await coordinator.async_config_entry_first_refresh()

    # store coordinator
    hass.data.setdefault(DOMAIN, {})
    hass.data[DOMAIN][entry.entry_id] = coordinator

    # forward to platforms
    await hass.config_entries.async_forward_entry_setups(
        entry,
        ["sensor", "binary_sensor"],
    )

    _LOGGER.info("Vibepollo Bridge initialized successfully")

    return True
