from unittest.mock import AsyncMock

from ui.controller import parse_raw, parse_result, send_start, send_stop
from ui.service import UIService


def test_parse_raw_roundtrip() -> None:
    payload = {
        "timestamps": [0.0, 0.1],
        "values": [1.0, -1.0],
        "sampling_rate_hz": 10.0,
        "correlation_id": "ui-1",
    }
    parsed = parse_raw(payload)
    assert parsed.correlation_id == "ui-1"
    assert parsed.timestamps == [0.0, 0.1]


def test_parse_result_roundtrip() -> None:
    payload = {
        "peak_frequencies_hz": [50.0],
        "health_score": 0.9,
        "correlation_id": "ui-2",
    }
    parsed = parse_result(payload)
    assert parsed.health_score == 0.9
    assert parsed.peak_frequencies_hz == [50.0]


async def test_send_start_publishes_command() -> None:
    publish = AsyncMock()
    await send_start(publish, 1000.0, 1.0, True, "ui-3")
    publish.assert_awaited_once()
    args, _ = publish.await_args
    assert args[0] == "cmd.start"
    assert args[1]["correlation_id"] == "ui-3"


async def test_send_stop_publishes_command() -> None:
    publish = AsyncMock()
    await send_stop(publish, "ui-4")
    publish.assert_awaited_once()
    args, _ = publish.await_args
    assert args[0] == "cmd.stop"


async def test_ui_service_send_start() -> None:
    service = UIService("amqp://test")
    service.exchange = AsyncMock()

    correlation_id = await service.send_start(1000.0, 1.0, True)

    assert correlation_id is not None
    service.exchange.publish.assert_awaited_once()
    args, kwargs = service.exchange.publish.await_args
    assert kwargs["routing_key"] == "cmd.start"


async def test_ui_service_send_stop() -> None:
    service = UIService("amqp://test")
    service.exchange = AsyncMock()

    await service.send_stop("test-corr-id")

    service.exchange.publish.assert_awaited_once()
    args, kwargs = service.exchange.publish.await_args
    assert kwargs["routing_key"] == "cmd.stop"


async def test_ui_service_send_shutdown_all() -> None:
    service = UIService("amqp://test")
    service.exchange = AsyncMock()

    await service.send_shutdown_all()

    service.exchange.publish.assert_awaited_once()
    args, kwargs = service.exchange.publish.await_args
    assert kwargs["routing_key"] == "cmd.shutdown"


async def test_ui_service_handle_shutdown() -> None:
    service = UIService("amqp://test")
    assert not service.should_shutdown

    await service._handle_shutdown({"correlation_id": "test-shutdown"})

    assert service.should_shutdown
