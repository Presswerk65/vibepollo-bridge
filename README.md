
# Vibepollo Bridge

Home Assistant custom integration for Vibepollo streaming servers.

## Features

- ✅ Live stream detection
- ✅ Active connections (from API)
- ✅ Dynamic client discovery
- ✅ Per-client binary sensors (connected / disconnected)
- ✅ Automatic entity creation
- ✅ Single device architecture
- ✅ Self‑signed HTTPS support

---

## Installation

### HACS (recommended)

1. Open HACS
2. Add custom repository:
https://github.com/Presswerk65/vibepollo-bridge

3. Category: **Integration**
4. Install
5. Restart Home Assistant

---

## Configuration

Add via UI:

- Host (name or IP)
- Token (more on that later)

---

## API Requirements

This integration requires access to:

### `/api/session/status`
Provides:
- activeSessions
- appName
- stream status

### `/api/clients/list`
Provides:
- connected clients
- client identities
- UUID-based tracking

---

## Entities

### Sensors

- `sensor.current_game`
- `sensor.active_connections`

### Binary Sensors

- `binary_sensor.client_<name>`

---

## Notes

- Multiple clients supported
- New clients are auto-discovered
- Uses UUID for reliable identification
- Updates every 5 seconds

---

## Configuration in Vibepollo
Under clients, create a new token with this API endpoints:
/api/clients/list
/api/session/status

Enter the token in the Vibepollo-Bridge Setup
