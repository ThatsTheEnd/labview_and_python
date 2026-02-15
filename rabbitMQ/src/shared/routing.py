"""Routing keys and exchange name for the demo topology."""

EXCHANGE_NAME = "demo.topic"

ROUTING_CMD_START = "cmd.start"
ROUTING_CMD_STOP = "cmd.stop"
ROUTING_CMD_SHUTDOWN = "cmd.shutdown"
ROUTING_MEAS_RAW = "meas.raw"
ROUTING_MEAS_RESULT = "meas.result"
ROUTING_STATUS_HEARTBEAT = "status.heartbeat"

# Queue names
QUEUE_LV = "lv.queue"
QUEUE_ANALYSIS = "analysis.queue"
QUEUE_UI = "ui.queue"
