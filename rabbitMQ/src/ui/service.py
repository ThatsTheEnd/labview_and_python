"""UI RabbitMQ service."""

from __future__ import annotations

import logging
import uuid
from typing import Any, Callable, Dict

import aio_pika

from shared import (
    BaseRabbitMQService,
    QUEUE_UI,
    ROUTING_CMD_SHUTDOWN,
    ROUTING_CMD_START,
    ROUTING_CMD_STOP,
    ROUTING_MEAS_RAW,
    ROUTING_MEAS_RESULT,
    ROUTING_STATUS_HEARTBEAT,
    get_rabbitmq_url,
    publish_json,
)
from shared.contracts import AnalysisResult, CommandStart, RawMeasurement

logger = logging.getLogger(__name__)

MessageHandler = Callable[[str, Dict[str, Any]], None]


class UIService(BaseRabbitMQService):
    def __init__(self, rabbitmq_url: str) -> None:
        super().__init__(rabbitmq_url, QUEUE_UI)
        self.raw_handler: MessageHandler | None = None
        self.result_handler: MessageHandler | None = None
        self.heartbeat_handler: MessageHandler | None = None

    def set_raw_handler(self, handler: MessageHandler) -> None:
        self.raw_handler = handler
        # Register wrapper that converts from (payload) to (routing_key, payload)
        self.register_handler(
            ROUTING_MEAS_RAW,
            lambda payload: self._invoke_handler(self.raw_handler, ROUTING_MEAS_RAW, payload),
        )

    def set_result_handler(self, handler: MessageHandler) -> None:
        self.result_handler = handler
        self.register_handler(
            ROUTING_MEAS_RESULT,
            lambda payload: self._invoke_handler(
                self.result_handler, ROUTING_MEAS_RESULT, payload
            ),
        )

    def set_heartbeat_handler(self, handler: MessageHandler) -> None:
        self.heartbeat_handler = handler
        self.register_handler(
            ROUTING_STATUS_HEARTBEAT,
            lambda payload: self._invoke_handler(
                self.heartbeat_handler, ROUTING_STATUS_HEARTBEAT, payload
            ),
        )

    @staticmethod
    def _invoke_handler(
        handler: MessageHandler | None, routing_key: str, payload: Dict[str, Any]
    ) -> None:
        """Invoke a handler with routing_key and payload."""
        if handler:
            handler(routing_key, payload)

    async def send_start(
        self,
        sampling_rate_hz: float,
        duration_s: float,
        fault_enabled: bool,
    ) -> str:
        correlation_id = str(uuid.uuid4())
        command = CommandStart(
            sampling_rate_hz=sampling_rate_hz,
            duration_s=duration_s,
            fault_enabled=fault_enabled,
            correlation_id=correlation_id,
        )

        if self.exchange:
            await publish_json(self.exchange, ROUTING_CMD_START, command.to_dict())
            logger.info("Sent cmd.start: correlation_id=%s", correlation_id)

        return correlation_id

    async def send_stop(self, correlation_id: str) -> None:
        payload = {"correlation_id": correlation_id}
        if self.exchange:
            await publish_json(self.exchange, ROUTING_CMD_STOP, payload)
            logger.info("Sent cmd.stop: correlation_id=%s", correlation_id)

    async def send_shutdown_all(self) -> None:
        correlation_id = str(uuid.uuid4())
        payload = {"correlation_id": correlation_id}
        if self.exchange:
            await publish_json(self.exchange, ROUTING_CMD_SHUTDOWN, payload)
            logger.info(
                "Sent cmd.shutdown to all modules: correlation_id=%s", correlation_id
            )
