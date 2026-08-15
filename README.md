# ael-architect

State model:

- Add-ons: `enabled = true|false`, `state = "loaded"|"none"`
- Packages: `enabled = true|false`, `state = "installed"|"uninstalled"`

`enabled` is desired state. `state` is cached last-known state.
Startup trusts cached state and only acts when desired/cached state disagree.
The Check button performs the expensive verification and updates `state`.
Removal/uninstallation is intentionally not implemented yet.
