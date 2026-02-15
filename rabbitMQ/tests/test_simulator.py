from unittest.mock import AsyncMock

from simulator.signal import generate_raw_measurement
from simulator.service import SimulatorService


def test_generate_raw_measurement_length_and_timestamps() -> None:
    result = generate_raw_measurement(
        sampling_rate_hz=1000.0,
        duration_s=1.0,
        fault_enabled=False,
        correlation_id="test-1",
    )
    assert len(result.timestamps) == 1000
    assert len(result.values) == 1000
    assert result.timestamps[0] == 0.0
    assert result.timestamps[-1] == 0.999


def test_generate_raw_measurement_deterministic() -> None:
    first = generate_raw_measurement(500.0, 1.0, False, "test-2")
    second = generate_raw_measurement(500.0, 1.0, False, "test-2")
    assert first.values == second.values


def test_fault_increases_peak_amplitude() -> None:
    no_fault = generate_raw_measurement(1000.0, 1.0, False, "test-3")
    with_fault = generate_raw_measurement(1000.0, 1.0, True, "test-4")
    assert max(with_fault.values) > max(no_fault.values)


async def test_simulator_service_handle_start() -> None:
    service = SimulatorService("amqp://test")
    service.exchange = AsyncMock()

    payload = {
        "sampling_rate_hz": 500.0,
        "duration_s": 0.5,
        "fault_enabled": False,
        "correlation_id": "test-sim-1",
    }

    await service._handle_start(payload)

    service.exchange.publish.assert_awaited_once()
    args, kwargs = service.exchange.publish.await_args
    assert kwargs["routing_key"] == "meas.raw"


async def test_simulator_service_handle_shutdown() -> None:
    service = SimulatorService("amqp://test")
    assert not service.should_shutdown

    await service._handle_shutdown({"correlation_id": "test-shutdown"})

    assert service.should_shutdown
