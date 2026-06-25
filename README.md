
# Vibepollo Bridge

Home Assistant custom integration for Vibepollo streaming servers.

## Features
- Live stream status
- Active connections via API
- Dynamic client detection
- Auto discovery of new clients
- Per-client binary sensors
- Single device architecture

## Installation (HACS)
Add this repository to HACS as Custom Repository.

## Manual Installation
Copy `custom_components/vibepollo_bridge` into your HA `config` directory.

Restart Home Assistant.

## Configuration in Vibepollo
Under clients, create a new token with this API endpoints:
/api/clients/list
/api/session/status

Enter the token in the Vibepollo-Bridge Setup
