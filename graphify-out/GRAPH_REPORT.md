# Graph Report - .  (2026-04-12)

## Corpus Check
- Corpus is ~3,218 words - fits in a single context window. You may not need a graph.

## Summary
- 117 nodes · 187 edges · 16 communities detected
- Extraction: 74% EXTRACTED · 26% INFERRED · 0% AMBIGUOUS · INFERRED: 49 edges (avg confidence: 0.53)
- Token cost: 0 input · 0 output

## Community Hubs (Navigation)
- [[_COMMUNITY_Core Data Models & Forwarder|Core Data Models & Forwarder]]
- [[_COMMUNITY_Protocol Handlers (UDPTCP)|Protocol Handlers (UDP/TCP)]]
- [[_COMMUNITY_NMEA Sentence Generation|NMEA Sentence Generation]]
- [[_COMMUNITY_MAVLink Reader & Polling|MAVLink Reader & Polling]]
- [[_COMMUNITY_Architecture Overview (Docs)|Architecture Overview (Docs)]]
- [[_COMMUNITY_FastAPI Endpoints & Routing|FastAPI Endpoints & Routing]]
- [[_COMMUNITY_Config Persistence|Config Persistence]]
- [[_COMMUNITY_Config Models (Docs)|Config Models (Docs)]]
- [[_COMMUNITY_Forwarding Architecture (Docs)|Forwarding Architecture (Docs)]]
- [[_COMMUNITY_FastAPI Framework (Docs)|FastAPI Framework (Docs)]]
- [[_COMMUNITY_Obsidian Export Script|Obsidian Export Script]]
- [[_COMMUNITY_Extension Identity|Extension Identity]]
- [[_COMMUNITY_Extension Identifier|Extension Identifier]]
- [[_COMMUNITY_Docker Image|Docker Image]]
- [[_COMMUNITY_Poll Rate Setting|Poll Rate Setting]]
- [[_COMMUNITY_Dashboard UI|Dashboard UI]]

## God Nodes (most connected - your core abstractions)
1. `MavlinkReader` - 18 edges
2. `NmeaForwarder` - 16 edges
3. `OutputConfig` - 15 edges
4. `GpsData` - 12 edges
5. `AppConfig` - 10 edges
6. `UdpHandler` - 7 edges
7. `TcpHandler` - 7 edges
8. `AddOutputRequest` - 7 edges
9. `UpdateOutputRequest` - 7 edges
10. `PollRateRequest` - 7 edges

## Surprising Connections (you probably didn't know these)
- `NMEA sentence forwarding to UDP/TCP endpoints.` --uses--> `OutputConfig`  [INFERRED]
  app\forwarder.py → app\config.py
- `Async MAVLink GPS data reader via mavlink2rest.` --uses--> `GpsData`  [INFERRED]
  app\mavlink_reader.py → app\nmea.py
- `Parse fix_type from mavlink2rest (can be int, string, or dict).` --uses--> `GpsData`  [INFERRED]
  app\mavlink_reader.py → app\nmea.py
- `Generate simulated GPS data that drifts slowly.` --uses--> `GpsData`  [INFERRED]
  app\mavlink_reader.py → app\nmea.py
- `OutputStats` --uses--> `OutputConfig`  [INFERRED]
  app\forwarder.py → app\config.py

## Hyperedges (group relationships)
- **MAVLink to NMEA Data Pipeline** — claudemd_mavlinkreader, claudemd_gpsdata, claudemd_gpgga, claudemd_gpzda, claudemd_nmeaforwarder [EXTRACTED 1.00]
- **Application Module Set** — claudemd_main_py, claudemd_mavlink_reader_py, claudemd_nmea_py, claudemd_forwarder_py, claudemd_config_py, claudemd_index_html [EXTRACTED 1.00]
- **Runtime Dependencies** — claudemd_fastapi, claudemd_httpx, claudemd_pydantic [EXTRACTED 1.00]
- **Protocol Handler Set** — claudemd_nmeaforwarder, claudemd_udphandler, claudemd_tcphandler [EXTRACTED 1.00]

## Communities

### Community 0 - "Core Data Models & Forwarder"
Cohesion: 0.3
Nodes (13): BaseModel, AppConfig, OutputConfig, NmeaForwarder, Send sentences to all enabled outputs. Returns number of successful sends., AddOutputRequest, GpzdaRequest, PollRateRequest (+5 more)

### Community 1 - "Protocol Handlers (UDP/TCP)"
Cohesion: 0.18
Nodes (4): OutputStats, NMEA sentence forwarding to UDP/TCP endpoints., TcpHandler, UdpHandler

### Community 2 - "NMEA Sentence Generation"
Cohesion: 0.18
Nodes (15): _compute_checksum(), _deg_e7_to_nmea_lat(), _deg_e7_to_nmea_lon(), _fix_type_to_gga_quality(), _format_utc_time(), generate_gpgga(), generate_gpzda(), NMEA sentence generation for GPGGA and GPZDA from MAVLink GPS data. (+7 more)

### Community 3 - "MAVLink Reader & Polling"
Cohesion: 0.16
Nodes (5): MavlinkReader, _parse_fix_type(), Async MAVLink GPS data reader via mavlink2rest., Generate simulated GPS data that drifts slowly., Parse fix_type from mavlink2rest (can be int, string, or dict).

### Community 4 - "Architecture Overview (Docs)"
Cohesion: 0.2
Nodes (14): BlueOS Platform, BlueOS NMEA Router Extension, Callback System Pattern, GPGGA Sentence, GPS_RAW_INT MAVLink Message, GpsData Dataclass, GPZDA Sentence, httpx Library (+6 more)

### Community 5 - "FastAPI Endpoints & Routing"
Cohesion: 0.23
Nodes (8): add_output(), broadcast_outputs_update(), get_status(), lifespan(), on_gps_update(), remove_output(), update_output(), websocket_endpoint()

### Community 6 - "Config Persistence"
Cohesion: 0.33
Nodes (5): load_config(), Configuration model and persistence for NMEA Router., Load config from disk, or return defaults if not found., Atomically save config to disk., save_config()

### Community 7 - "Config Models (Docs)"
Cohesion: 0.33
Nodes (6): AppConfig Model, Atomic Config Writes Pattern, config.py Module, OutputConfig Model, Pydantic Library, Rationale: Atomic Writes Prevent Corruption

### Community 8 - "Forwarding Architecture (Docs)"
Cohesion: 0.47
Nodes (6): forwarder.py Module, NmeaForwarder Class, Rationale: TCP Persistent Connections with Retry, Rationale: UDP is Fire-and-Forget, TcpHandler Class, UdpHandler Class

### Community 9 - "FastAPI Framework (Docs)"
Cohesion: 1.0
Nodes (2): FastAPI Framework, main.py Module

### Community 10 - "Obsidian Export Script"
Cohesion: 1.0
Nodes (0): 

### Community 11 - "Extension Identity"
Cohesion: 1.0
Nodes (1): BlueOS NMEA Router Extension (README)

### Community 12 - "Extension Identifier"
Cohesion: 1.0
Nodes (1): Extension Identifier ryaan354.blueos-nmea-forwarding

### Community 13 - "Docker Image"
Cohesion: 1.0
Nodes (1): Docker Image ryaan354/blueos-nmea-forwarding

### Community 14 - "Poll Rate Setting"
Cohesion: 1.0
Nodes (1): Configurable Poll Rate (0.1-10 Hz)

### Community 15 - "Dashboard UI"
Cohesion: 1.0
Nodes (1): static/index.html Dashboard

## Knowledge Gaps
- **27 isolated node(s):** `Configuration model and persistence for NMEA Router.`, `Load config from disk, or return defaults if not found.`, `Atomically save config to disk.`, `NMEA sentence generation for GPGGA and GPZDA from MAVLink GPS data.`, `XOR all characters between $ and * (exclusive), return 2-char hex.` (+22 more)
  These have ≤1 connection - possible missing edges or undocumented components.
- **Thin community `FastAPI Framework (Docs)`** (2 nodes): `FastAPI Framework`, `main.py Module`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Obsidian Export Script`** (1 nodes): `_graphify_obsidian.py`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Extension Identity`** (1 nodes): `BlueOS NMEA Router Extension (README)`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Extension Identifier`** (1 nodes): `Extension Identifier ryaan354.blueos-nmea-forwarding`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Docker Image`** (1 nodes): `Docker Image ryaan354/blueos-nmea-forwarding`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Poll Rate Setting`** (1 nodes): `Configurable Poll Rate (0.1-10 Hz)`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Dashboard UI`** (1 nodes): `static/index.html Dashboard`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.

## Suggested Questions
_Questions this graph is uniquely positioned to answer:_

- **Why does `GpsData` connect `Core Data Models & Forwarder` to `NMEA Sentence Generation`, `MAVLink Reader & Polling`?**
  _High betweenness centrality (0.188) - this node is a cross-community bridge._
- **Why does `OutputConfig` connect `Core Data Models & Forwarder` to `Protocol Handlers (UDP/TCP)`, `Config Persistence`?**
  _High betweenness centrality (0.143) - this node is a cross-community bridge._
- **Why does `MavlinkReader` connect `MAVLink Reader & Polling` to `Core Data Models & Forwarder`?**
  _High betweenness centrality (0.116) - this node is a cross-community bridge._
- **Are the 8 inferred relationships involving `MavlinkReader` (e.g. with `AddOutputRequest` and `UpdateOutputRequest`) actually correct?**
  _`MavlinkReader` has 8 INFERRED edges - model-reasoned connections that need verification._
- **Are the 8 inferred relationships involving `NmeaForwarder` (e.g. with `OutputConfig` and `AddOutputRequest`) actually correct?**
  _`NmeaForwarder` has 8 INFERRED edges - model-reasoned connections that need verification._
- **Are the 13 inferred relationships involving `OutputConfig` (e.g. with `OutputStats` and `UdpHandler`) actually correct?**
  _`OutputConfig` has 13 INFERRED edges - model-reasoned connections that need verification._
- **Are the 11 inferred relationships involving `GpsData` (e.g. with `AddOutputRequest` and `UpdateOutputRequest`) actually correct?**
  _`GpsData` has 11 INFERRED edges - model-reasoned connections that need verification._