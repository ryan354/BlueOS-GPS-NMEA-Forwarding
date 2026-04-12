# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## What This Is

A BlueOS extension that reads GPS data from MAVLink (via mavlink2rest), converts it to NMEA 0183 sentences (GPGGA, GPZDA), and forwards them over UDP/TCP to configurable output destinations.

## Build & Run

Dependencies are managed directly in the Dockerfile (no requirements.txt). Runtime deps: `fastapi`, `uvicorn`, `httpx`, `pydantic`.

**Docker Compose (production-like):**
```bash
docker-compose up
# Access at http://localhost:8080
```

**Direct Python (development, auto-reloads):**
```bash
pip install fastapi uvicorn httpx pydantic
python app/main.py
# Access at http://localhost:8000
```

There are no tests or linting configured.

## Architecture

```
MAVLink (mavlink2rest :6040)
  → MavlinkReader (HTTP polling via httpx)
    → GpsData (parsed GPS_RAW_INT)
      → NMEA sentence generation (GPGGA + GPZDA)
        → NmeaForwarder (UDP/TCP broadcast to outputs)
          → WebSocket broadcast to dashboard clients
```

**Key modules in `app/`:**
- **main.py** — FastAPI app, REST API, WebSocket endpoint (`/ws`), BlueOS service registration, global state and lifespan management
- **mavlink_reader.py** — `MavlinkReader` class, async HTTP polling of mavlink2rest with exponential backoff, callback-based GPS update notifications
- **nmea.py** — `GpsData` dataclass, NMEA sentence generators (`generate_gpgga`, `generate_gpzda`), coordinate conversion (degE7 → ddmm.mmmmm), checksum computation
- **forwarder.py** — `NmeaForwarder` with `UdpHandler` (stateless) and `TcpHandler` (stateful with retry), per-output stats tracking
- **config.py** — Pydantic models (`OutputConfig`, `AppConfig`), atomic JSON persistence (temp file + rename), `CONFIG_DIR` env var (default `/app/data`)
- **static/index.html** — Single-page vanilla JS dashboard, no build step, served as static file

## Key Patterns

- **Callback system**: `MavlinkReader` notifies subscribers (forwarder + WebSocket clients) on each GPS update
- **Atomic config writes**: config.py uses temp file + os.replace to prevent corruption
- **Protocol handlers**: UDP is fire-and-forget; TCP maintains persistent connections with retry logic
- **BlueOS integration**: Docker labels in Dockerfile define extension metadata for the BlueOS Extension Manager; service registration via `/register_service` endpoint on startup

## graphify

This project has a graphify knowledge graph at graphify-out/.

Rules:
- Before answering architecture or codebase questions, read graphify-out/GRAPH_REPORT.md for god nodes and community structure
- If graphify-out/wiki/index.md exists, navigate it instead of reading raw files
- After modifying code files in this session, run `python3 -c "from graphify.watch import _rebuild_code; from pathlib import Path; _rebuild_code(Path('.'))"` to keep the graph current
