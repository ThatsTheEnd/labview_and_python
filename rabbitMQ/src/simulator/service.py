"""Simulator RabbitMQ service."""

from __future__ import annotations

import logging
from typing import Any, Dict

from shared import (
    BaseRabbitMQService,
    QUEUE_LV,
    ROUTING_CMD_SHUTDOWN,
    ROUTING_CMD_START,
    ROUTING_CMD_STOP,
    ROUTING_MEAS_RAW,
    get_rabbitmq_url,
    publish_json,
)
from shared.contracts import CommandStart

from .signal import generate_raw_measurement

logger = logging.getLogger(__name__)


class SimulatorService(BaseRabbitMQService):
    def __init__(self, rabbitmq_url: str) -> None:
        super().__init__(rabbitmq_url, QUEUE_LV)
        self.register_handler(ROUTING_CMD_START, self._handle_start)
        self.register_handler(ROUTING_CMD_STOP, self._handle_stop)

    async def _handle_start(self, payload: Dict[str, Any]) -> None:
        cmd = CommandStart.from_dict(payload)
        logger.info(
            "Received cmd.start: correlation_id=%s, rate=%.1f Hz, duration=%.1f s, fault=%s",
            cmd.correlation_id,
            cmd.sampling_rate_hz,
            cmd.duration_s,
            cmd.fault_enabled,
        )

        measurement = generate_raw_measurement(
            sampling_rate_hz=cmd.sampling_rate_hz,
            duration_s=cmd.duration_s,
            fault_enabled=cmd.fault_enabled,
            correlation_id=cmd.correlation_id,
        )

        if self.exchange:
            await publish_json(self.exchange, ROUTING_MEAS_RAW, measurement.to_dict())
            logger.info("Published meas.raw with %d samples", len(measurement.values))

    async def _handle_stop(self, payload: Dict[str, Any]) -> None:
        correlation_id = payload.get("correlation_id", "unknown")
        logger.info("Received cmd.stop: correlation_id=%s", correlation_id)

