---
type: community
cohesion: 0.33
members: 6
---

# Config Persistence

**Cohesion:** 0.33 - loosely connected
**Members:** 6 nodes

## Members
- [[Atomically save config to disk.]] - rationale - app\config.py
- [[Configuration model and persistence for NMEA Router.]] - rationale - app\config.py
- [[Load config from disk, or return defaults if not found.]] - rationale - app\config.py
- [[config.py]] - code - app\config.py
- [[load_config()]] - code - app\config.py
- [[save_config()]] - code - app\config.py

## Live Query (requires Dataview plugin)

```dataview
TABLE source_file, type FROM #community/Config_Persistence
SORT file.name ASC
```

## Connections to other communities
- 3 edges to [[_COMMUNITY_Core Data Models & Forwarder]]

## Top bridge nodes
- [[config.py]] - degree 5, connects to 1 community
- [[load_config()]] - degree 3, connects to 1 community