"""Async MAVLink GPS data reader via mavlink2rest."""
from __future__ import annotations

import asyncio
import logging
import math
import random
from datetime import datetime, timezone
from typing import Callable, Any, Optional, List

import httpx

from nmea import GpsData, generate_gpgga, generate_gpzda

logger = logging.getLogger(__name__)

# MAVLink fix_type enum strings from mavlink2rest
FIX_TYPE_MAP = {
    "NoGps": 0, "NO_GPS": 0,
    "NoFix": 1, "NO_FIX": 1,
    "Fix2d": 2, "2D_FIX": 2, "D2Fix": 2,
    "Fix3d": 3, "3D_FIX": 3, "D3Fix": 3,
    "Dgps": 4, "DGPS": 4,
    "RtkFloat": 5, "RTK_FLOAT": 5,
    "RtkFixed": 6, "RTK_FIXED": 6,
    "Static": 7, "STATIC": 7,
    "Ppp": 8, "PPP": 8,
}

FIX_TYPE_NAMES = {
    0: "No GPS", 1: "No Fix", 2: "2D Fix", 3: "3D Fix",
    4: "DGPS", 5: "RTK Float", 6: "RTK Fixed", 7: "Static", 8: "PPP",
}


def _parse_fix_type(val: Any) -> int:
    """Parse fix_type from mavlink2rest (can be int, string, or dict)."""
    if isinstance(val, int):
        return val
    if isinstance(val, str):
        return FIX_TYPE_MAP.get(val, 0)
    if isinstance(val, dict):
        return FIX_TYPE_MAP.get(val.get("type", ""), 0)
    return 0


class MavlinkReader:
    def __init__(self, mavlink_url: str = "http://host.docker.internal:6040", dummy: bool = False):
        self.mavlink_url = mavlink_url.rstrip("/")
        self.endpoint = (
            f"{self.mavlink_url}/v1/mavlink/vehicles/1/components/1/messages/GPS_RAW_INT"
        )
        self.dummy = dummy
        self.poll_rate_hz: float = 1.0
        self.latest_gps: Optional[GpsData] = None
        self.latest_gpgga: str = ""
        self.latest_gpzda: str = ""
        self.connected: bool = False
        self.error_message: Optional[str] = None
        self._task: Optional[asyncio.Task] = None
        self._callbacks: List[Callable] = []
        self._client: Optional[httpx.AsyncClient] = None
        self._running: bool = False

    def add_callback(self, fn: Callable) -> None:
        self._callbacks.append(fn)

    def remove_callback(self, fn: Callable) -> None:
        self._callbacks.remove(fn)

    async def start(self, poll_rate_hz: float = 1.0) -> None:
        self.poll_rate_hz = poll_rate_hz
        self._running = True
        self._client = httpx.AsyncClient(timeout=5.0)
        self._task = asyncio.create_task(self._poll_loop())
        logger.info("MavlinkReader started at %.1f Hz", poll_rate_hz)

    async def stop(self) -> None:
        self._running = False
        if self._task:
            self._task.cancel()
            try:
                await self._task
            except asyncio.CancelledError:
                pass
        if self._client:
            await self._client.aclose()
        logger.info("MavlinkReader stopped")

    def set_poll_rate(self, hz: float) -> None:
        self.poll_rate_hz = max(1.0, min(hz, 20.0))

    def get_status(self) -> dict:
        gps = self.latest_gps
        if gps is None:
            return {
                "connected": self.connected,
                "fix_type": 0,
                "fix_type_name": "No GPS",
                "lat": 0.0,
                "lon": 0.0,
                "alt": 0.0,
                "satellites": 0,
                "hdop": 99.99,
                "speed": 0.0,
                "course": 0.0,
                "error": self.error_message,
            }
        return {
            "connected": self.connected,
            "fix_type": gps.fix_type,
            "fix_type_name": FIX_TYPE_NAMES.get(gps.fix_type, "Unknown"),
            "lat": gps.lat / 1e7,
            "lon": gps.lon / 1e7,
            "alt": gps.alt / 1000.0,
            "satellites": gps.satellites,
            "hdop": gps.eph / 100.0 if gps.eph > 0 else 99.99,
            "speed": gps.vel / 100.0,
            "course": gps.cog / 100.0,
            "error": None,
        }

    def _generate_dummy_gps(self) -> GpsData:
        """Generate simulated GPS data that drifts slowly."""
        t = asyncio.get_event_loop().time()
        # Simulate a slow circle around a base position
        base_lat = -33.8688 * 1e7   # Sydney, Australia
        base_lon = 151.2093 * 1e7
        radius = 500 * 1e7 / 111139  # ~500m radius in degE7
        lat = int(base_lat + radius * math.sin(t * 0.05))
        lon = int(base_lon + radius * math.cos(t * 0.05))
        alt = int((50.0 + 5.0 * math.sin(t * 0.1)) * 1000)  # ~50m altitude in mm
        vel = int((1.5 + 0.5 * math.sin(t * 0.2)) * 100)    # ~1.5 m/s in cm/s
        cog = int(((math.degrees(math.atan2(math.cos(t * 0.05), -math.sin(t * 0.05))) % 360) * 100))
        return GpsData(
            lat=lat, lon=lon, alt=alt,
            fix_type=3,  # 3D Fix
            satellites=random.randint(8, 14),
            eph=random.randint(80, 150),
            epv=random.randint(100, 200),
            vel=vel, cog=cog,
            time_usec=int(datetime.now(timezone.utc).timestamp() * 1e6),
        )

    async def _poll_loop(self) -> None:
        backoff = 1.0
        while self._running:
            try:
                if self.dummy:
                    gps = self._generate_dummy_gps()
                else:
                    resp = await self._client.get(self.endpoint)
                    resp.raise_for_status()
                    data = resp.json()

                    msg = data.get("message", data)
                    gps = GpsData(
                        lat=msg.get("lat", 0),
                        lon=msg.get("lon", 0),
                        alt=msg.get("alt", 0),
                        fix_type=_parse_fix_type(msg.get("fix_type", 0)),
                        satellites=msg.get("satellites_visible", 0),
                        eph=msg.get("eph", 0),
                        epv=msg.get("epv", 0),
                        vel=msg.get("vel", 0),
                        cog=msg.get("cog", 0),
                        time_usec=msg.get("time_usec", 0),
                    )

                self.latest_gps = gps
                self.connected = True
                self.error_message = None
                backoff = 1.0

                utc = datetime.now(timezone.utc)
                self.latest_gpgga = generate_gpgga(gps, utc)
                self.latest_gpzda = generate_gpzda(utc)

                for cb in self._callbacks:
                    try:
                        result = cb(gps, self.latest_gpgga, self.latest_gpzda)
                        if asyncio.iscoroutine(result):
                            await result
                    except Exception as e:
                        logger.warning("Callback error: %s", e)

            except httpx.HTTPStatusError as e:
                self.connected = False
                self.error_message = f"HTTP {e.response.status_code}"
                logger.warning("mavlink2rest HTTP error: %s", e)
                backoff = min(backoff * 1.5, 10.0)
            except (httpx.ConnectError, httpx.TimeoutException) as e:
                self.connected = False
                self.error_message = f"Connection failed: {type(e).__name__}"
                logger.warning("mavlink2rest connection error: %s", e)
                backoff = min(backoff * 1.5, 10.0)
            except Exception as e:
                self.connected = False
                self.error_message = str(e)
                logger.exception("Unexpected error in poll loop")
                backoff = min(backoff * 1.5, 10.0)

            interval = 1.0 / self.poll_rate_hz if self.connected else backoff
            await asyncio.sleep(interval)
