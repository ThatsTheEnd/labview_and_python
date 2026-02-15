from shared.contracts import CommandStart
from shared.routing import (
    EXCHANGE_NAME,
    ROUTING_CMD_START,
    ROUTING_CMD_STOP,
    ROUTING_MEAS_RAW,
    ROUTING_MEAS_RESULT,
    ROUTING_STATUS_HEARTBEAT,
)


def test_routing_constants() -> None:
    assert EXCHANGE_NAME == "demo.topic"
    assert ROUTING_CMD_START == "cmd.start"
    assert ROUTING_CMD_STOP == "cmd.stop"
    assert ROUTING_MEAS_RAW == "meas.raw"
    assert ROUTING_MEAS_RESULT == "meas.result"
    assert ROUTING_STATUS_HEARTBEAT == "status.heartbeat"


def test_command_start_roundtrip() -> None:
    msg = CommandStart(
        sampling_rate_hz=1000.0,
        duration_s=2.0,
        fault_enabled=True,
        correlation_id="abc-123",
    )
    payload = msg.to_dict()
    loaded = CommandStart.from_dict(payload)
    assert loaded == msg
