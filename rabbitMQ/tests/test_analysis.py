from unittest.mock import AsyncMock

from analysis.processing import analyze_measurement
from analysis.service import AnalysisService
from shared.contracts import RawMeasurement


def test_analyze_measurement_basic_peaks() -> None:
    measurement = RawMeasurement(
        timestamps=[0.0, 0.001, 0.002, 0.003],
        values=[0.0, 1.0, 0.0, -1.0],
        sampling_rate_hz=1000.0,
        correlation_id="test-1",
    )
    result = analyze_measurement(measurement, peak_count=1)
    assert result.correlation_id == "test-1"
    assert len(result.peak_frequencies_hz) == 1


def test_health_score_range() -> None:
    measurement = RawMeasurement(
        timestamps=[0.0, 0.001, 0.002, 0.003],
        values=[0.0, 1.0, 0.0, -1.0],
        sampling_rate_hz=1000.0,
        correlation_id="test-2",
    )
    result = analyze_measurement(measurement)
    assert 0.0 <= result.health_score <= 1.0


async def test_analysis_service_handle_raw() -> None:
    service = AnalysisService("amqp://test")
    service.exchange = AsyncMock()

    payload = {
        "timestamps": [0.0, 0.001, 0.002, 0.003],
        "values": [0.0, 1.0, 0.0, -1.0],
        "sampling_rate_hz": 1000.0,
        "correlation_id": "test-analysis-1",
    }

    await service._handle_raw(payload)

    service.exchange.publish.assert_awaited_once()
    args, kwargs = service.exchange.publish.await_args
    assert kwargs["routing_key"] == "meas.result"


async def test_analysis_service_handle_shutdown() -> None:
    service = AnalysisService("amqp://test")
    assert not service.should_shutdown

    await service._handle_shutdown({"correlation_id": "test-shutdown"})

    assert service.should_shutdown
