---
type: community
cohesion: 0.18
members: 16
---

# NMEA Sentence Generation

**Cohesion:** 0.18 - loosely connected
**Members:** 16 nodes

## Members
- [[Convert degE7 latitude to NMEA ddmm.mmmm format and NS indicator.]] - rationale - app\nmea.py
- [[Convert degE7 longitude to NMEA dddmm.mmmm format and EW indicator.]] - rationale - app\nmea.py
- [[Format datetime to NMEA hhmmss.ss.]] - rationale - app\nmea.py
- [[Generate a GPGGA sentence from GPS data.]] - rationale - app\nmea.py
- [[Generate a GPZDA sentence from current UTC time.]] - rationale - app\nmea.py
- [[Map MAVLink fix_type to NMEA GGA quality indicator.]] - rationale - app\nmea.py
- [[NMEA sentence generation for GPGGA and GPZDA from MAVLink GPS data.]] - rationale - app\nmea.py
- [[XOR all characters between $ and  (exclusive), return 2-char hex.]] - rationale - app\nmea.py
- [[_compute_checksum()]] - code - app\nmea.py
- [[_deg_e7_to_nmea_lat()]] - code - app\nmea.py
- [[_deg_e7_to_nmea_lon()]] - code - app\nmea.py
- [[_fix_type_to_gga_quality()]] - code - app\nmea.py
- [[_format_utc_time()]] - code - app\nmea.py
- [[generate_gpgga()]] - code - app\nmea.py
- [[generate_gpzda()]] - code - app\nmea.py
- [[nmea.py]] - code - app\nmea.py

## Live Query (requires Dataview plugin)

```dataview
TABLE source_file, type FROM #community/NMEA_Sentence_Generation
SORT file.name ASC
```

## Connections to other communities
- 1 edge to [[_COMMUNITY_Core Data Models & Forwarder]]

## Top bridge nodes
- [[nmea.py]] - degree 9, connects to 1 community