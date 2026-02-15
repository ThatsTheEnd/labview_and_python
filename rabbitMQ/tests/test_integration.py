from analysis.processing import analyze_measurement
from simulator.signal import generate_raw_measurement


def test_simulator_to_analysis_flow() -> None:
    measurement = generate_raw_measurement(
        sampling_rate_hz=1000.0,
        duration_s=1.0,
        fault_enabled=False,
        correlation_id="integration-1",
    )
    result = analyze_measurement(measurement)
    assert result.correlation_id == "integration-1"
    assert any(abs(freq - 50.0) < 1.0 for freq in result.peak_frequencies_hz)


def test_fault_reduces_health_score() -> None:
    no_fault = generate_raw_measurement(
        sampling_rate_hz=1000.0,
        duration_s=1.0,
        fault_enabled=False,
        correlation_id="integration-2",
    )
    with_fault = generate_raw_measurement(
        sampling_rate_hz=1000.0,
        duration_s=1.0,
        fault_enabled=True,
        correlation_id="integration-3",
    )
    result_no_fault = analyze_measurement(no_fault)
    result_fault = analyze_measurement(with_fault)
    assert result_fault.health_score < result_no_fault.health_score
