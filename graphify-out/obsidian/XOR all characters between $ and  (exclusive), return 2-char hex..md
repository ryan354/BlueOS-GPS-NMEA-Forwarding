---
source_file: "app\nmea.py"
type: "rationale"
community: "NMEA Sentence Generation"
location: "L24"
tags:
  - graphify/rationale
  - graphify/EXTRACTED
  - community/NMEA_Sentence_Generation
---

# XOR all characters between $ and * (exclusive), return 2-char hex.

## Connections
- [[_compute_checksum()]] - `rationale_for` [EXTRACTED]

#graphify/rationale #graphify/EXTRACTED #community/NMEA_Sentence_Generation