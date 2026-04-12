---
source_file: "app\nmea.py"
type: "code"
community: "NMEA Sentence Generation"
location: "L23"
tags:
  - graphify/code
  - graphify/EXTRACTED
  - community/NMEA_Sentence_Generation
---

# _compute_checksum()

## Connections
- [[XOR all characters between $ and  (exclusive), return 2-char hex.]] - `rationale_for` [EXTRACTED]
- [[generate_gpgga()]] - `calls` [EXTRACTED]
- [[generate_gpzda()]] - `calls` [EXTRACTED]
- [[nmea.py]] - `contains` [EXTRACTED]

#graphify/code #graphify/EXTRACTED #community/NMEA_Sentence_Generation