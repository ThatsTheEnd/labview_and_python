"""Typed message contracts shared across modules."""

from __future__ import annotations

from dataclasses import dataclass
from typing import Any, Dict, List, Mapping, Sequence, cast


@dataclass(frozen=True)
class CommandStart:
    sampling_rate_hz: float
    duration_s: float
    fault_enabled: bool
    correlation_id: str

    def to_dict(self) -> Dict[str, object]:
        return {
            "sampling_rate_hz": self.sampling_rate_hz,
            "duration_s": self.duration_s,
            "fault_enabled": self.fault_enabled,
            "correlation_id": self.correlation_id,
        }

    @classmethod
    def from_dict(cls, data: Mapping[str, Any]) -> "CommandStart":
        return cls(
            sampling_rate_hz=float(data["sampling_rate_hz"]),
            duration_s=float(data["duration_s"]),
            fault_enabled=bool(data["fault_enabled"]),
            correlation_id=str(data["correlation_id"]),
        )


@dataclass(frozen=True)
class RawMeasurement:
    timestamps: List[float]
    values: List[float]
    sampling_rate_hz: float
    correlation_id: str

    def to_dict(self) -> Dict[str, object]:
        return {
            "timestamps": list(self.timestamps),
            "values": list(self.values),
            "sampling_rate_hz": self.sampling_rate_hz,
            "correlation_id": self.correlation_id,
        }

    @classmethod
    def from_dict(cls, data: Mapping[str, Any]) -> "RawMeasurement":
        timestamps = cast(Sequence[float], data["timestamps"])
        values = cast(Sequence[float], data["values"])
        return cls(
            timestamps=[float(x) for x in timestamps],
            values=[float(x) for x in values],
            sampling_rate_hz=float(data["sampling_rate_hz"]),
            correlation_id=str(data["correlation_id"]),
        )


@dataclass(frozen=True)
class AnalysisResult:
    peak_frequencies_hz: List[float]
    health_score: float
    correlation_id: str

    def to_dict(self) -> Dict[str, object]:
        return {
            "peak_frequencies_hz": list(self.peak_frequencies_hz),
            "health_score": self.health_score,
            "correlation_id": self.correlation_id,
        }

    @classmethod
    def from_dict(cls, data: Mapping[str, Any]) -> "AnalysisResult":
        peaks = cast(Sequence[float], data["peak_frequencies_hz"])
        return cls(
            peak_frequencies_hz=[float(x) for x in peaks],
            health_score=float(data["health_score"]),
            correlation_id=str(data["correlation_id"]),
        )
