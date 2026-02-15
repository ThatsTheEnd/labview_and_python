"""Analysis RabbitMQ service."""

from __future__ import annotations

import logging
from typing import Any, Dict

from shared import (
    BaseRabbitMQService,
    QUEUE_ANALYSIS,
    ROUTING_CMD_SHUTDOWN,
    ROUTING_MEAS_RAW,
    ROUTING_MEAS_RESULT,
    get_rabbitmq_url,
    publish_json,
)
from shared.contracts import RawMeasurement

from .processing import analyze_measurement

logger = logging.getLogger(__name__)


class AnalysisService(BaseRabbitMQService):
    def __init__(self, rabbitmq_url: str) -> None:
        super().__init__(rabbitmq_url, QUEUE_ANALYSIS)
        self.register_handler(ROUTING_MEAS_RAW, self._handle_raw)

    async def _handle_raw(self, payload: Dict[str, Any]) -> None:
        measurement = RawMeasurement.from_dict(payload)
        logger.info(
            "Received meas.raw: correlation_id=%s, samples=%d",
            measurement.correlation_id,
            len(measurement.values),
        )

        result = analyze_measurement(measurement)

        if self.exchange:
            await publish_json(self.exchange, ROUTING_MEAS_RESULT, result.to_dict())
            logger.info(
                "Published meas.result: correlation_id=%s, health=%.2f, peaks=%d",
                result.correlation_id,
                result.health_score,
                len(result.peak_frequencies_hz),
            )

