"""Signal analysis for demo measurements."""

from __future__ import annotations

from typing import List

import numpy as np

from shared.contracts import AnalysisResult, RawMeasurement


def analyze_measurement(
    measurement: RawMeasurement,
    peak_count: int = 3,
) -> AnalysisResult:
    frequencies, magnitudes = _fft_spectrum(
        measurement.values, measurement.sampling_rate_hz
    )
    peak_frequencies = _top_peaks(frequencies, magnitudes, peak_count)
    health_score = _health_score(frequencies, magnitudes)

    return AnalysisResult(
        peak_frequencies_hz=peak_frequencies,
        health_score=health_score,
        correlation_id=measurement.correlation_id,
    )


def _fft_spectrum(values: List[float], sampling_rate_hz: float) -> tuple[np.ndarray, np.ndarray]:
    data = np.asarray(values, dtype=float)
    spectrum = np.fft.rfft(data)
    magnitudes = np.abs(spectrum)
    frequencies = np.fft.rfftfreq(data.size, d=1.0 / sampling_rate_hz)
    return frequencies, magnitudes


def _top_peaks(
    frequencies: np.ndarray,
    magnitudes: np.ndarray,
    peak_count: int,
) -> List[float]:
    if frequencies.size == 0:
        return []

    mags = magnitudes.copy()
    mags[0] = 0.0

    peak_indices = np.argsort(mags)[::-1][:peak_count]
    peaks = sorted(float(frequencies[idx]) for idx in peak_indices)
    return peaks


def _health_score(
    frequencies: np.ndarray,
    magnitudes: np.ndarray,
    fault_band: tuple[float, float] = (250.0, 350.0),
) -> float:
    if frequencies.size == 0:
        return 1.0

    total_energy = float(np.sum(magnitudes))
    if total_energy == 0.0:
        return 1.0

    low, high = fault_band
    mask = (frequencies >= low) & (frequencies <= high)
    fault_energy = float(np.sum(magnitudes[mask]))
    penalty = min(1.0, fault_energy / total_energy)
    return max(0.0, 1.0 - penalty)
