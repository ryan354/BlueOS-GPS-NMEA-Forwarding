# BlueOS NMEA Router Extension

A BlueOS extension that converts MAVLink GPS data (GPS_RAW_INT) to NMEA sentences (GPGGA, GPZDA) and forwards them to configurable UDP/TCP endpoints.

## Features

- Reads GPS data from mavlink2rest (GPS_RAW_INT message)
- Generates standard NMEA 0183 sentences: GPGGA (fix data) and GPZDA (date/time)
- Forward NMEA output to multiple UDP/TCP endpoints simultaneously
- Real-time web dashboard with GPS status, NMEA monitor, and output management
- Configurable poll rate (0.1 - 10 Hz)
- Persistent configuration across restarts

## Installation on BlueOS

### From Extensions Manager (manual install)

1. Go to **Extensions Manager** in BlueOS
2. Click the **Installed** tab, then the **+** icon
3. Fill in:
   - **Extension Identifier**: `ryaan354.blueos-nmea-forwarding`
   - **Extension Name**: `NMEA GPS Forwarding`
   - **Docker image**: `ryaan354/blueos-nmea-forwarding`
   - **Docker tag**: `latest`
   - **Custom settings**:
     ```json
     {
       "ExposedPorts": {"80/tcp": {}},
       "HostConfig": {
         "ExtraHosts": ["host.docker.internal:host-gateway"],
         "PortBindings": {"80/tcp": [{"HostPort": ""}]},
         "Binds": ["/usr/blueos/extensions/nmea-router:/app/data"]
       }
     }
     ```

## Local Development

```bash
docker compose up --build
```

Open http://localhost:8080

## Architecture

- **Backend**: Python + FastAPI + uvicorn
- **Frontend**: Single-page HTML with WebSocket for real-time updates
- **Data flow**: mavlink2rest → GPS_RAW_INT → NMEA conversion → UDP/TCP forwarding
