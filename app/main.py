"""BlueOS NMEA Router Extension - FastAPI Application."""
from __future__ import annotations

import asyncio
import logging
from contextlib import asynccontextmanager
from datetime import datetime, timezone
from typing import Literal, Optional, Set

from fastapi import FastAPI, WebSocket, WebSocketDisconnect
from fastapi.staticfiles import StaticFiles
from fastapi.responses import JSONResponse
from pydantic import BaseModel

from config import AppConfig, OutputConfig, load_config, save_config
from mavlink_reader import MavlinkReader
from forwarder import NmeaForwarder
from nmea import GpsData

logging.basicConfig(level=logging.INFO, format="%(asctime)s [%(name)s] %(levelname)s: %(message)s")
logger = logging.getLogger("nmea-router")


async def broadcast_outputs_update():
    """Push current output list to all WebSocket clients immediately."""
    msg = {
        "type": "outputs_update",
        "outputs": forwarder.get_output_statuses(),
    }
    dead = set()
    for ws in ws_clients:
        try:
            await ws.send_json(msg)
        except Exception:
            dead.add(ws)
    ws_clients.difference_update(dead)

# Global state
config: AppConfig = AppConfig()
reader: MavlinkReader = MavlinkReader()
forwarder: NmeaForwarder = NmeaForwarder()
ws_clients: Set[WebSocket] = set()


async def on_gps_update(gps: GpsData, gpgga: str, gpzda: str):
    """Called by MavlinkReader on each GPS update."""
    # Forward to all outputs
    await forwarder.broadcast([gpgga, gpzda])

    # Push to all WebSocket clients
    msg = {
        "type": "update",
        "gps": reader.get_status(),
        "nmea": {"gpgga": gpgga, "gpzda": gpzda},
        "outputs": forwarder.get_output_statuses(),
        "timestamp": datetime.now(timezone.utc).isoformat(),
    }
    dead = set()
    for ws in ws_clients:
        try:
            await ws.send_json(msg)
        except Exception:
            dead.add(ws)
    ws_clients.difference_update(dead)


@asynccontextmanager
async def lifespan(app: FastAPI):
    global config, reader, forwarder
    # Startup
    config = load_config()
    reader = MavlinkReader(mavlink_url=config.mavlink_url)
    reader.add_callback(on_gps_update)

    for out in config.outputs:
        forwarder.add_output(out)

    await reader.start(config.poll_rate_hz)
    logger.info("NMEA Router started with %d outputs", len(config.outputs))

    yield

    # Shutdown
    await reader.stop()
    forwarder.close_all()
    logger.info("NMEA Router stopped")


app = FastAPI(title="NMEA Router", lifespan=lifespan)


# ──────────────────── BlueOS Service Registration ────────────────────

@app.get("/register_service")
async def register_service():
    return {
        "name": "NMEA Router",
        "description": "MAVLink GPS to NMEA (GPGGA/GPZDA) forwarder via UDP/TCP",
        "icon": "mdi-satellite-variant",
        "company": "Rovostech",
        "version": "1.0.0",
        "new_page": False,
        "webpage": "https://github.com/ryan354/BlueOS-GPS-NMEA-Forwarding",
        "api": "/docs",
    }


# ──────────────────── REST API ────────────────────

@app.get("/api/v1/status")
async def get_status():
    return {
        "gps": reader.get_status(),
        "outputs": forwarder.get_output_statuses(),
        "poll_rate_hz": reader.poll_rate_hz,
    }


@app.get("/api/v1/config")
async def get_config():
    return config.model_dump()


class AddOutputRequest(BaseModel):
    name: str = "Untitled"
    protocol: Literal["udp", "tcp"] = "udp"
    host: str = "127.0.0.1"
    port: int = 10110
    enabled: bool = True


@app.post("/api/v1/outputs")
async def add_output(req: AddOutputRequest):
    out = OutputConfig(
        name=req.name,
        protocol=req.protocol,
        host=req.host,
        port=req.port,
        enabled=req.enabled,
    )
    config.outputs.append(out)
    forwarder.add_output(out)
    save_config(config)
    await broadcast_outputs_update()
    return out.model_dump()


@app.delete("/api/v1/outputs/{output_id}")
async def remove_output(output_id: str):
    config.outputs = [o for o in config.outputs if o.id != output_id]
    forwarder.remove_output(output_id)
    save_config(config)
    await broadcast_outputs_update()
    return {"status": "ok"}


class UpdateOutputRequest(BaseModel):
    name: Optional[str] = None
    host: Optional[str] = None
    port: Optional[int] = None
    enabled: Optional[bool] = None


@app.put("/api/v1/outputs/{output_id}")
async def update_output(output_id: str, req: UpdateOutputRequest):
    for out in config.outputs:
        if out.id == output_id:
            if req.name is not None:
                out.name = req.name
            if req.host is not None:
                out.host = req.host
            if req.port is not None:
                out.port = req.port
            if req.enabled is not None:
                out.enabled = req.enabled
                forwarder.update_output(output_id, req.enabled)
            save_config(config)
            await broadcast_outputs_update()
            return out.model_dump()
    return JSONResponse({"error": "not found"}, status_code=404)


class PollRateRequest(BaseModel):
    hz: float


@app.put("/api/v1/poll_rate")
async def set_poll_rate(req: PollRateRequest):
    config.poll_rate_hz = max(0.1, min(req.hz, 10.0))
    reader.set_poll_rate(config.poll_rate_hz)
    save_config(config)
    return {"poll_rate_hz": config.poll_rate_hz}


# ──────────────────── WebSocket ────────────────────

@app.websocket("/api/v1/ws")
async def websocket_endpoint(ws: WebSocket):
    await ws.accept()
    ws_clients.add(ws)
    logger.info("WebSocket client connected (%d total)", len(ws_clients))
    try:
        # Send initial state
        await ws.send_json({
            "type": "init",
            "gps": reader.get_status(),
            "outputs": forwarder.get_output_statuses(),
            "poll_rate_hz": reader.poll_rate_hz,
        })
        # Keep alive - wait for client disconnect
        while True:
            await ws.receive_text()
    except WebSocketDisconnect:
        pass
    finally:
        ws_clients.discard(ws)
        logger.info("WebSocket client disconnected (%d remaining)", len(ws_clients))


# ──────────────────── Static Files (must be last) ────────────────────

app.mount("/", StaticFiles(directory="static", html=True), name="static")
