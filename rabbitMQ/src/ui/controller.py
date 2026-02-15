"""UI-side helpers for publishing commands and parsing results."""

from __future__ import annotations

from typing import Any, Awaitable, Callable, Mapping

from shared.contracts import AnalysisResult, CommandStart, RawMeasurement
from shared.routing import ROUTING_CMD_START, ROUTING_CMD_STOP

PublishFn = Callable[[str, Mapping[str, Any]], Awaitable[None]]


async def send_start(
    publish: PublishFn,
    sampling_rate_hz: float,
    duration_s: float,
    fault_enabled: bool,
    correlation_id: str,
) -> None:
    message = CommandStart(
        sampling_rate_hz=sampling_rate_hz,
        duration_s=duration_s,
        fault_enabled=fault_enabled,
        correlation_id=correlation_id,
    )
    await publish(ROUTING_CMD_START, message.to_dict())


async def send_stop(
    publish: PublishFn,
    correlation_id: str,
) -> None:
    payload = {"correlation_id": correlation_id}
    await publish(ROUTING_CMD_STOP, payload)


def parse_raw(payload: Mapping[str, Any]) -> RawMeasurement:
    return RawMeasurement.from_dict(payload)


def parse_result(payload: Mapping[str, Any]) -> AnalysisResult:
    return AnalysisResult.from_dict(payload)
