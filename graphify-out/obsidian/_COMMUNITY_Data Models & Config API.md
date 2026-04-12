---
type: community
cohesion: 0.30
members: 17
---

# Data Models & Config API

**Cohesion:** 0.30 - loosely connected
**Members:** 17 nodes

## Members
- [[.__init__()_2]] - code - app\forwarder.py
- [[.broadcast()]] - code - app\forwarder.py
- [[.get_output_statuses()]] - code - app\forwarder.py
- [[.update_output()]] - code - app\forwarder.py
- [[AddOutputRequest]] - code - app\main.py
- [[AppConfig]] - code - app\config.py
- [[BaseModel]] - code
- [[BlueOS NMEA Router Extension - FastAPI Application.]] - rationale - app\main.py
- [[Called by MavlinkReader on each GPS update.]] - rationale - app\main.py
- [[GpsData]] - code - app\nmea.py
- [[GpzdaRequest]] - code - app\main.py
- [[NmeaForwarder]] - code - app\forwarder.py
- [[OutputConfig]] - code - app\config.py
- [[PollRateRequest]] - code - app\main.py
- [[Push current output list to all WebSocket clients immediately.]] - rationale - app\main.py
- [[Send sentences to all enabled outputs. Returns number of successful sends.]] - rationale - app\forwarder.py
- [[UpdateOutputRequest]] - code - app\main.py

## Live Query (requires Dataview plugin)

```dataview
TABLE source_file, type FROM #community/Data_Models_&_Config_API
SORT file.name ASC
```

## Connections to other communities
- 11 edges to [[_COMMUNITY_MAVLink Reader & Polling]]
- 8 edges to [[_COMMUNITY_Protocol Handlers (UDPTCP)]]
- 7 edges to [[_COMMUNITY_FastAPI Endpoints & Routing]]
- 3 edges to [[_COMMUNITY_Config Persistence]]
- 1 edge to [[_COMMUNITY_NMEA Sentence Generation]]

## Top bridge nodes
- [[OutputConfig]] - degree 15, connects to 2 communities
- [[GpsData]] - degree 12, connects to 2 communities
- [[AddOutputRequest]] - degree 7, connects to 2 communities
- [[GpzdaRequest]] - degree 7, connects to 2 communities
- [[PollRateRequest]] - degree 7, connects to 2 communities