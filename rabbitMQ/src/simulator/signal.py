"""Signal generation for the LabVIEW simulator stub."""

from __future__ import annotations

from typing import List

import numpy as np

from shared.contracts import RawMeasurement


def generate_raw_measurement(
    sampling_rate_hz: float,
    duration_s: float,
    fault_enabled: bool,
    correlation_id: str,
) -> RawMeasurement:
    sample_count = int(sampling_rate_hz * duration_s)
    timestamps = np.arange(sample_count, dtype=float) / sampling_rate_hz

    base = np.sin(2.0 * np.pi * 50.0 * timestamps)
    harmonic = 0.3 * np.sin(2.0 * np.pi * 120.0 * timestamps)
    drift = 0.05 * np.sin(2.0 * np.pi * 7.0 * timestamps)

    signal = base + harmonic + drift

    if fault_enabled:
        start = int(sample_count * 0.6)
        end = int(sample_count * 0.7)
        burst = 0.8 * np.sin(2.0 * np.pi * 300.0 * timestamps)
        signal[start:end] += burst[start:end]

    return RawMeasurement(
        timestamps=timestamps.tolist(),
        values=signal.tolist(),
        sampling_rate_hz=sampling_rate_hz,
        correlation_id=correlation_id,
    )
