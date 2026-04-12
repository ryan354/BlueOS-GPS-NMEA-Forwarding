---
source_file: "app\main.py"
type: "rationale"
community: "Core Data Models & Forwarder"
location: "L47"
tags:
  - graphify/rationale
  - graphify/INFERRED
  - community/Core_Data_Models_&_Forwarder
---

# Called by MavlinkReader on each GPS update.

## Connections
- [[AppConfig]] - `uses` [INFERRED]
- [[GpsData]] - `uses` [INFERRED]
- [[MavlinkReader]] - `uses` [INFERRED]
- [[NmeaForwarder]] - `uses` [INFERRED]
- [[OutputConfig]] - `uses` [INFERRED]
- [[on_gps_update()]] - `rationale_for` [EXTRACTED]

#graphify/rationale #graphify/INFERRED #community/Core_Data_Models_&_Forwarder