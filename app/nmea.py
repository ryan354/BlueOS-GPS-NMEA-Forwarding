"""NMEA sentence generation for GPGGA and GPZDA from MAVLink GPS data."""

from __future__ import annotations
from datetime import datetime, timezone
from dataclasses import dataclass
from typing import Optional


@dataclass
class GpsData:
    lat: int           # degE7
    lon: int           # degE7
    alt: int           # mm (MSL)
    fix_type: int      # 0-6
    satellites: int
    eph: int           # HDOP * 100 (65535 = unknown)
    epv: int           # VDOP * 100 (65535 = unknown)
    vel: int           # ground speed cm/s
    cog: int           # course over ground cdeg
    time_usec: int = 0


def _compute_checksum(body: str) -> str:
    """XOR all characters between $ and * (exclusive), return 2-char hex."""
    cs = 0
    for ch in body:
        cs ^= ord(ch)
    return f"{cs:02X}"


def _deg_e7_to_nmea_lat(deg_e7: int) -> tuple[str, str]:
    """Convert degE7 latitude to NMEA ddmm.mmmm format and N/S indicator."""
    hemisphere = "N" if deg_e7 >= 0 else "S"
    deg_e7 = abs(deg_e7)
    degrees = deg_e7 // 10_000_000
    remainder = deg_e7 % 10_000_000
    minutes = remainder * 60.0 / 10_000_000
    return f"{degrees:02d}{minutes:07.4f}", hemisphere


def _deg_e7_to_nmea_lon(deg_e7: int) -> tuple[str, str]:
    """Convert degE7 longitude to NMEA dddmm.mmmm format and E/W indicator."""
    hemisphere = "E" if deg_e7 >= 0 else "W"
    deg_e7 = abs(deg_e7)
    degrees = deg_e7 // 10_000_000
    remainder = deg_e7 % 10_000_000
    minutes = remainder * 60.0 / 10_000_000
    return f"{degrees:03d}{minutes:07.4f}", hemisphere


def _fix_type_to_gga_quality(fix_type: int) -> int:
    """Map MAVLink fix_type to NMEA GGA quality indicator."""
    mapping = {
        0: 0,  # No GPS
        1: 0,  # No fix
        2: 1,  # 2D fix
        3: 1,  # 3D fix
        4: 2,  # DGPS
        5: 5,  # RTK float
        6: 4,  # RTK fixed
    }
    return mapping.get(fix_type, 0)


def _format_utc_time(utc: datetime) -> str:
    """Format datetime to NMEA hhmmss.ss."""
    return f"{utc.hour:02d}{utc.minute:02d}{utc.second:02d}.{utc.microsecond // 10000:02d}"


def generate_gpgga(gps: GpsData, utc: Optional[datetime] = None) -> str:
    """Generate a GPGGA sentence from GPS data."""
    if utc is None:
        utc = datetime.now(timezone.utc)

    time_str = _format_utc_time(utc)
    lat_str, lat_ns = _deg_e7_to_nmea_lat(gps.lat)
    lon_str, lon_ew = _deg_e7_to_nmea_lon(gps.lon)
    quality = _fix_type_to_gga_quality(gps.fix_type)

    # Handle unknown satellite count (255 = UINT8_MAX)
    sats = gps.satellites if gps.satellites < 255 else 0

    # Handle unknown HDOP (65535 = UINT16_MAX)
    if gps.eph > 0 and gps.eph < 65535:
        hdop_str = f"{gps.eph / 100.0:.1f}"
    else:
        hdop_str = "99.9"

    alt_m = gps.alt / 1000.0

    # Geoid separation left empty when unknown — avoids INS rejecting
    # a bogus 0.0 value that implies ellipsoid == MSL
    body = (
        f"GPGGA,{time_str},{lat_str},{lat_ns},{lon_str},{lon_ew},"
        f"{quality},{sats:02d},{hdop_str},{alt_m:.1f},M,,M,,"
    )
    checksum = _compute_checksum(body)
    return f"${body}*{checksum}"


def generate_gpzda(utc: Optional[datetime] = None) -> str:
    """Generate a GPZDA sentence from current UTC time."""
    if utc is None:
        utc = datetime.now(timezone.utc)

    time_str = _format_utc_time(utc)
    body = f"GPZDA,{time_str},{utc.day:02d},{utc.month:02d},{utc.year:04d},00,00"
    checksum = _compute_checksum(body)
    return f"${body}*{checksum}"
