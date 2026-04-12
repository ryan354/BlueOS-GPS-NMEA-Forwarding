---
type: community
cohesion: 0.18
members: 16
---

# Protocol Handlers (UDP/TCP)

**Cohesion:** 0.18 - loosely connected
**Members:** 16 nodes

## Members
- [[.__init__()_1]] - code - app\forwarder.py
- [[.__init__()]] - code - app\forwarder.py
- [[._connect()]] - code - app\forwarder.py
- [[._ensure_socket()]] - code - app\forwarder.py
- [[.add_output()]] - code - app\forwarder.py
- [[.close()_1]] - code - app\forwarder.py
- [[.close()]] - code - app\forwarder.py
- [[.close_all()]] - code - app\forwarder.py
- [[.remove_output()]] - code - app\forwarder.py
- [[.send()_1]] - code - app\forwarder.py
- [[.send()]] - code - app\forwarder.py
- [[NMEA sentence forwarding to UDPTCP endpoints.]] - rationale - app\forwarder.py
- [[OutputStats]] - code - app\forwarder.py
- [[TcpHandler]] - code - app\forwarder.py
- [[UdpHandler]] - code - app\forwarder.py
- [[forwarder.py]] - code - app\forwarder.py

## Live Query (requires Dataview plugin)

```dataview
TABLE source_file, type FROM #community/Protocol_Handlers_(UDP/TCP)
SORT file.name ASC
```

## Connections to other communities
- 8 edges to [[_COMMUNITY_Core Data Models & Forwarder]]

## Top bridge nodes
- [[TcpHandler]] - degree 7, connects to 1 community
- [[UdpHandler]] - degree 7, connects to 1 community
- [[forwarder.py]] - degree 5, connects to 1 community
- [[OutputStats]] - degree 4, connects to 1 community
- [[.add_output()]] - degree 3, connects to 1 community