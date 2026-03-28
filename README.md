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

## Running the Service

### Option 1: Docker Compose (Production-like)
Runs the service in a Docker container, matching the deployed environment.

```bash
docker-compose up
```

- Access UI at `http://localhost:8080`
- Logs stream to terminal
- Press `Ctrl+C` to stop

For background mode:
```bash
docker-compose up -d
docker-compose logs -f  # follow logs separately
```

### Option 2: Python Direct (Fastest Development)
Runs the app locally without Docker. Changes reload automatically.

```bash
# Install dependencies (one-time)
pip install fastapi uvicorn httpx pydantic

# Run the app
python app/main.py
```

- Access UI at `http://localhost:8000`
- Code changes auto-reload (no rebuild needed)
- Faster iteration for debugging

### Option 3: VS Code Debugger
Enable step-through debugging with breakpoints.

Create `.vscode/launch.json`:
```json
{
  "version": "0.2.0",
  "configurations": [
    {
      "name": "Python: FastAPI",
      "type": "python",
      "request": "launch",
      "program": "${workspaceFolder}/app/main.py",
      "console": "integratedTerminal",
      "justMyCode": true
    }
  ]
}
```

Press `F5` to start debugging. Set breakpoints in the code.

**Which to use?**
- **Option 2** during development (fastest feedback loop)
- **Option 1** before pushing to verify container works
- **Option 3** for step-through debugging

## Architecture

- **Backend**: Python + FastAPI + uvicorn
- **Frontend**: Single-page HTML with WebSocket for real-time updates
- **Data flow**: mavlink2rest → GPS_RAW_INT → NMEA conversion → UDP/TCP forwarding
