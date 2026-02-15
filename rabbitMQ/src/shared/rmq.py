"""RabbitMQ helper functions for exchange/queue setup and JSON messaging."""

from __future__ import annotations

import json
import os
from typing import Any, Mapping

import aio_pika
from aio_pika.abc import (
    AbstractChannel,
    AbstractExchange,
    AbstractQueue,
    AbstractRobustConnection,
)

from .routing import (
    EXCHANGE_NAME,
    QUEUE_ANALYSIS,
    QUEUE_LV,
    QUEUE_UI,
    ROUTING_CMD_SHUTDOWN,
    ROUTING_MEAS_RAW,
    ROUTING_MEAS_RESULT,
)


async def connect(url: str) -> AbstractRobustConnection:
    return await aio_pika.connect_robust(url)


async def setup_exchange(
    channel: AbstractChannel,
    exchange_name: str,
) -> AbstractExchange:
    return await channel.declare_exchange(
        exchange_name,
        aio_pika.ExchangeType.TOPIC,
        durable=True,
    )


async def declare_queue(channel: AbstractChannel, queue_name: str) -> AbstractQueue:
    return await channel.declare_queue(queue_name, durable=True)


async def bind_queue(
    queue: AbstractQueue,
    exchange: AbstractExchange,
    routing_key: str,
) -> None:
    await queue.bind(exchange, routing_key)


async def publish_json(
    exchange: AbstractExchange,
    routing_key: str,
    payload: Mapping[str, Any],
) -> None:
    body = json.dumps(payload).encode("utf-8")
    message = aio_pika.Message(body=body, content_type="application/json")
    await exchange.publish(message, routing_key=routing_key)


def parse_json(body: bytes) -> dict[str, Any]:
    return json.loads(body.decode("utf-8"))


def get_rabbitmq_url() -> str:
    return os.environ.get("RABBITMQ_URL", "amqp://guest:guest@localhost/")


async def provision_topology(channel: AbstractChannel) -> None:
    exchange = await setup_exchange(channel, EXCHANGE_NAME)

    lv_queue = await declare_queue(channel, QUEUE_LV)
    analysis_queue = await declare_queue(channel, QUEUE_ANALYSIS)
    ui_queue = await declare_queue(channel, QUEUE_UI)

    await bind_queue(lv_queue, exchange, "cmd.*")
    await bind_queue(analysis_queue, exchange, ROUTING_MEAS_RAW)
    await bind_queue(analysis_queue, exchange, ROUTING_CMD_SHUTDOWN)
    await bind_queue(ui_queue, exchange, ROUTING_MEAS_RAW)
    await bind_queue(ui_queue, exchange, ROUTING_MEAS_RESULT)
    await bind_queue(ui_queue, exchange, "status.*")
    await bind_queue(ui_queue, exchange, ROUTING_CMD_SHUTDOWN)
