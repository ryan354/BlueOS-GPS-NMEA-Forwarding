"""Configuration model and persistence for NMEA Router."""
from __future__ import annotations

import json
import os
import tempfile
import uuid
from typing import Literal, List

from pydantic import BaseModel, Field


class OutputConfig(BaseModel):
    id: str = Field(default_factory=lambda: str(uuid.uuid4())[:8])
    name: str = "Untitled"
    protocol: Literal["udp", "tcp"] = "udp"
    host: str = "127.0.0.1"
    port: int = 10110
    enabled: bool = True


class AppConfig(BaseModel):
    poll_rate_hz: float = 5.0
    mavlink_url: str = "http://host.docker.internal:6040"
    outputs: List[OutputConfig] = Field(default_factory=list)


CONFIG_DIR = os.environ.get("CONFIG_DIR", "/app/data")
CONFIG_FILE = os.path.join(CONFIG_DIR, "config.json")


def load_config() -> AppConfig:
    """Load config from disk, or return defaults if not found."""
    try:
        with open(CONFIG_FILE, "r") as f:
            data = json.load(f)
        return AppConfig(**data)
    except (FileNotFoundError, json.JSONDecodeError, Exception):
        return AppConfig()


def save_config(config: AppConfig) -> None:
    """Atomically save config to disk."""
    os.makedirs(CONFIG_DIR, exist_ok=True)
    data = config.model_dump()
    fd, tmp_path = tempfile.mkstemp(dir=CONFIG_DIR, suffix=".tmp")
    try:
        with os.fdopen(fd, "w") as f:
            json.dump(data, f, indent=2)
        # On Windows, need to remove target first; on Linux rename is atomic
        if os.path.exists(CONFIG_FILE):
            os.replace(tmp_path, CONFIG_FILE)
        else:
            os.rename(tmp_path, CONFIG_FILE)
    except Exception:
        if os.path.exists(tmp_path):
            os.unlink(tmp_path)
        raise
