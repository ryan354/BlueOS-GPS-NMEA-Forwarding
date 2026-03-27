"""NMEA sentence forwarding to UDP/TCP endpoints."""
from __future__ import annotations

import asyncio
import logging
import socket
from dataclasses import dataclass, field
from typing import Optional, Dict, List, Union

from config import OutputConfig

logger = logging.getLogger(__name__)


@dataclass
class OutputStats:
    sentences_sent: int = 0
    errors: int = 0
    connected: bool = False


class UdpHandler:
    def __init__(self, config: OutputConfig):
        self.config = config
        self.stats = OutputStats(connected=True)  # UDP is "always connected"
        self._sock: Optional[socket.socket] = None

    def _ensure_socket(self) -> socket.socket:
        if self._sock is None:
            self._sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        return self._sock

    def send(self, sentence: str) -> bool:
        try:
            sock = self._ensure_socket()
            data = (sentence + "\r\n").encode("ascii")
            sock.sendto(data, (self.config.host, self.config.port))
            self.stats.sentences_sent += 1
            self.stats.connected = True
            return True
        except Exception as e:
            self.stats.errors += 1
            logger.warning("UDP send error to %s:%d: %s", self.config.host, self.config.port, e)
            return False

    def close(self) -> None:
        if self._sock:
            self._sock.close()
            self._sock = None


class TcpHandler:
    def __init__(self, config: OutputConfig):
        self.config = config
        self.stats = OutputStats()
        self._sock: Optional[socket.socket] = None
        self._connecting: bool = False

    def _connect(self) -> bool:
        if self._connecting:
            return False
        self._connecting = True
        try:
            self.close()
            sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            sock.settimeout(2.0)
            sock.connect((self.config.host, self.config.port))
            sock.settimeout(1.0)
            self._sock = sock
            self.stats.connected = True
            logger.info("TCP connected to %s:%d", self.config.host, self.config.port)
            return True
        except Exception as e:
            self.stats.connected = False
            logger.warning("TCP connect failed %s:%d: %s", self.config.host, self.config.port, e)
            return False
        finally:
            self._connecting = False

    def send(self, sentence: str) -> bool:
        if not self.stats.connected or self._sock is None:
            if not self._connect():
                self.stats.errors += 1
                return False
        try:
            data = (sentence + "\r\n").encode("ascii")
            self._sock.sendall(data)
            self.stats.sentences_sent += 1
            return True
        except Exception as e:
            self.stats.errors += 1
            self.stats.connected = False
            self._sock = None
            logger.warning("TCP send error to %s:%d: %s", self.config.host, self.config.port, e)
            return False

    def close(self) -> None:
        if self._sock:
            try:
                self._sock.close()
            except Exception:
                pass
            self._sock = None
            self.stats.connected = False


class NmeaForwarder:
    def __init__(self):
        self._handlers: Dict[str, Union[UdpHandler, TcpHandler]] = {}
        self._loop: Optional[asyncio.AbstractEventLoop] = None

    def add_output(self, config: OutputConfig) -> None:
        if config.protocol == "udp":
            self._handlers[config.id] = UdpHandler(config)
        elif config.protocol == "tcp":
            self._handlers[config.id] = TcpHandler(config)

    def remove_output(self, output_id: str) -> None:
        handler = self._handlers.pop(output_id, None)
        if handler:
            handler.close()

    def update_output(self, output_id: str, enabled: bool) -> None:
        handler = self._handlers.get(output_id)
        if handler:
            handler.config.enabled = enabled

    async def broadcast(self, sentences: List[str]) -> int:
        """Send sentences to all enabled outputs. Returns number of successful sends."""
        loop = asyncio.get_event_loop()
        sent = 0
        for handler in self._handlers.values():
            if not handler.config.enabled:
                continue
            for sentence in sentences:
                try:
                    success = await loop.run_in_executor(None, handler.send, sentence)
                    if success:
                        sent += 1
                except Exception as e:
                    logger.warning("Broadcast error: %s", e)
        return sent

    def get_output_statuses(self) -> list[dict]:
        statuses = []
        for handler in self._handlers.values():
            statuses.append({
                "id": handler.config.id,
                "name": handler.config.name,
                "protocol": handler.config.protocol,
                "host": handler.config.host,
                "port": handler.config.port,
                "enabled": handler.config.enabled,
                "connected": handler.stats.connected,
                "sentences_sent": handler.stats.sentences_sent,
                "errors": handler.stats.errors,
            })
        return statuses

    def close_all(self) -> None:
        for handler in self._handlers.values():
            handler.close()
        self._handlers.clear()
