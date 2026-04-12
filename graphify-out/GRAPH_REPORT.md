# Graph Report - .  (2026-04-12)

## Corpus Check
- 6 files · ~3,218 words
- Verdict: corpus is large enough that graph structure adds value.

## Summary
- 84 nodes · 155 edges · 7 communities detected
- Extraction: 71% EXTRACTED · 29% INFERRED · 0% AMBIGUOUS · INFERRED: 45 edges (avg confidence: 0.5)
- Token cost: 0 input · 0 output

## Community Hubs (Navigation)
- [[_COMMUNITY_Community 0|Community 0]]
- [[_COMMUNITY_Community 1|Community 1]]
- [[_COMMUNITY_Community 2|Community 2]]
- [[_COMMUNITY_Community 3|Community 3]]
- [[_COMMUNITY_Community 4|Community 4]]
- [[_COMMUNITY_Community 5|Community 5]]
- [[_COMMUNITY_Community 6|Community 6]]

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

## Communities

### Community 0 - "Community 0"
Cohesion: 0.3
Nodes (13): BaseModel, AppConfig, OutputConfig, NmeaForwarder, Send sentences to all enabled outputs. Returns number of successful sends., AddOutputRequest, GpzdaRequest, PollRateRequest (+5 more)

### Community 1 - "Community 1"
Cohesion: 0.18
Nodes (4): OutputStats, NMEA sentence forwarding to UDP/TCP endpoints., TcpHandler, UdpHandler

### Community 2 - "Community 2"
Cohesion: 0.18
Nodes (15): _compute_checksum(), _deg_e7_to_nmea_lat(), _deg_e7_to_nmea_lon(), _fix_type_to_gga_quality(), _format_utc_time(), generate_gpgga(), generate_gpzda(), NMEA sentence generation for GPGGA and GPZDA from MAVLink GPS data. (+7 more)

### Community 3 - "Community 3"
Cohesion: 0.16
Nodes (5): MavlinkReader, _parse_fix_type(), Async MAVLink GPS data reader via mavlink2rest., Generate simulated GPS data that drifts slowly., Parse fix_type from mavlink2rest (can be int, string, or dict).

### Community 4 - "Community 4"
Cohesion: 0.23
Nodes (8): add_output(), broadcast_outputs_update(), get_status(), lifespan(), on_gps_update(), remove_output(), update_output(), websocket_endpoint()

### Community 5 - "Community 5"
Cohesion: 0.33
Nodes (5): load_config(), Configuration model and persistence for NMEA Router., Load config from disk, or return defaults if not found., Atomically save config to disk., save_config()

### Community 6 - "Community 6"
Cohesion: 1.0
Nodes (0): 

## Knowledge Gaps
- **11 isolated node(s):** `Configuration model and persistence for NMEA Router.`, `Load config from disk, or return defaults if not found.`, `Atomically save config to disk.`, `NMEA sentence generation for GPGGA and GPZDA from MAVLink GPS data.`, `XOR all characters between $ and * (exclusive), return 2-char hex.` (+6 more)
  These have ≤1 connection - possible missing edges or undocumented components.
- **Thin community `Community 6`** (1 nodes): `_graphify_obsidian.py`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.

## Suggested Questions
_Questions this graph is uniquely positioned to answer:_

- **Why does `GpsData` connect `Community 0` to `Community 2`, `Community 3`?**
  _High betweenness centrality (0.368) - this node is a cross-community bridge._
- **Why does `OutputConfig` connect `Community 0` to `Community 1`, `Community 5`?**
  _High betweenness centrality (0.280) - this node is a cross-community bridge._
- **Why does `MavlinkReader` connect `Community 3` to `Community 0`?**
  _High betweenness centrality (0.227) - this node is a cross-community bridge._
- **Are the 8 inferred relationships involving `MavlinkReader` (e.g. with `AddOutputRequest` and `UpdateOutputRequest`) actually correct?**
  _`MavlinkReader` has 8 INFERRED edges - model-reasoned connections that need verification._
- **Are the 8 inferred relationships involving `NmeaForwarder` (e.g. with `OutputConfig` and `AddOutputRequest`) actually correct?**
  _`NmeaForwarder` has 8 INFERRED edges - model-reasoned connections that need verification._
- **Are the 13 inferred relationships involving `OutputConfig` (e.g. with `OutputStats` and `UdpHandler`) actually correct?**
  _`OutputConfig` has 13 INFERRED edges - model-reasoned connections that need verification._
- **Are the 11 inferred relationships involving `GpsData` (e.g. with `AddOutputRequest` and `UpdateOutputRequest`) actually correct?**
  _`GpsData` has 11 INFERRED edges - model-reasoned connections that need verification._