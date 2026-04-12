---
source_file: "app\main.py"
type: "rationale"
community: "Core Data Models & Forwarder"
location: "L26"
tags:
  - graphify/rationale
  - graphify/INFERRED
  - community/Core_Data_Models_&_Forwarder
---

# Push current output list to all WebSocket clients immediately.

## Connections
- [[AppConfig]] - `uses` [INFERRED]
- [[GpsData]] - `uses` [INFERRED]
- [[MavlinkReader]] - `uses` [INFERRED]
- [[NmeaForwarder]] - `uses` [INFERRED]
- [[OutputConfig]] - `uses` [INFERRED]
- [[broadcast_outputs_update()]] - `rationale_for` [EXTRACTED]

#graphify/rationale #graphify/INFERRED #community/Core_Data_Models_&_Forwarder