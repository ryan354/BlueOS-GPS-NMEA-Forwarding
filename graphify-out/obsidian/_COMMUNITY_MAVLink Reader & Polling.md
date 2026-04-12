---
type: community
cohesion: 0.16
members: 15
---

# MAVLink Reader & Polling

**Cohesion:** 0.16 - loosely connected
**Members:** 15 nodes

## Members
- [[.__init__()_3]] - code - app\mavlink_reader.py
- [[._generate_dummy_gps()]] - code - app\mavlink_reader.py
- [[._poll_loop()]] - code - app\mavlink_reader.py
- [[.add_callback()]] - code - app\mavlink_reader.py
- [[.get_status()]] - code - app\mavlink_reader.py
- [[.remove_callback()]] - code - app\mavlink_reader.py
- [[.set_poll_rate()]] - code - app\mavlink_reader.py
- [[.start()]] - code - app\mavlink_reader.py
- [[.stop()]] - code - app\mavlink_reader.py
- [[Async MAVLink GPS data reader via mavlink2rest.]] - rationale - app\mavlink_reader.py
- [[Generate simulated GPS data that drifts slowly.]] - rationale - app\mavlink_reader.py
- [[MavlinkReader]] - code - app\mavlink_reader.py
- [[Parse fix_type from mavlink2rest (can be int, string, or dict).]] - rationale - app\mavlink_reader.py
- [[_parse_fix_type()]] - code - app\mavlink_reader.py
- [[mavlink_reader.py]] - code - app\mavlink_reader.py

## Live Query (requires Dataview plugin)

```dataview
TABLE source_file, type FROM #community/MAVLink_Reader_&_Polling
SORT file.name ASC
```

## Connections to other communities
- 11 edges to [[_COMMUNITY_Core Data Models & Forwarder]]

## Top bridge nodes
- [[MavlinkReader]] - degree 18, connects to 1 community
- [[Async MAVLink GPS data reader via mavlink2rest.]] - degree 2, connects to 1 community
- [[Generate simulated GPS data that drifts slowly.]] - degree 2, connects to 1 community
- [[Parse fix_type from mavlink2rest (can be int, string, or dict).]] - degree 2, connects to 1 community