import json
import os
from unittest.mock import AsyncMock

import aio_pika

from shared.rmq import (
    bind_queue,
    declare_queue,
    get_rabbitmq_url,
    parse_json,
    provision_topology,
    publish_json,
    setup_exchange,
)


def test_parse_json_roundtrip() -> None:
    payload = {"value": 123, "flag": True}
    body = json.dumps(payload).encode("utf-8")
    assert parse_json(body) == payload


async def test_setup_exchange_calls_channel() -> None:
    channel = AsyncMock()
    await setup_exchange(channel, "demo.topic")
    channel.declare_exchange.assert_awaited_once_with(
        "demo.topic",
        aio_pika.ExchangeType.TOPIC,
        durable=True,
    )


async def test_declare_queue_calls_channel() -> None:
    channel = AsyncMock()
    await declare_queue(channel, "queue.name")
    channel.declare_queue.assert_awaited_once_with("queue.name", durable=True)


async def test_bind_queue_calls_bind() -> None:
    queue = AsyncMock()
    exchange = AsyncMock()
    await bind_queue(queue, exchange, "cmd.start")
    queue.bind.assert_awaited_once_with(exchange, "cmd.start")


async def test_publish_json_calls_exchange() -> None:
    exchange = AsyncMock()
    payload = {"a": 1}
    await publish_json(exchange, "meas.raw", payload)
    exchange.publish.assert_awaited_once()
    args, kwargs = exchange.publish.await_args
    message = args[0]
    assert isinstance(message, aio_pika.Message)
    assert kwargs["routing_key"] == "meas.raw"
    assert json.loads(message.body.decode("utf-8")) == payload


def test_get_rabbitmq_url_default() -> None:
    old_val = os.environ.get("RABBITMQ_URL")
    if "RABBITMQ_URL" in os.environ:
        del os.environ["RABBITMQ_URL"]
    try:
        assert get_rabbitmq_url() == "amqp://guest:guest@localhost/"
    finally:
        if old_val is not None:
            os.environ["RABBITMQ_URL"] = old_val


def test_get_rabbitmq_url_from_env() -> None:
    old_val = os.environ.get("RABBITMQ_URL")
    os.environ["RABBITMQ_URL"] = "amqp://custom:pass@remote:5672/"
    try:
        assert get_rabbitmq_url() == "amqp://custom:pass@remote:5672/"
    finally:
        if old_val is not None:
            os.environ["RABBITMQ_URL"] = old_val
        else:
            del os.environ["RABBITMQ_URL"]


async def test_provision_topology_creates_queues_and_bindings() -> None:
    channel = AsyncMock()
    exchange_mock = AsyncMock()
    lv_queue_mock = AsyncMock()
    analysis_queue_mock = AsyncMock()
    ui_queue_mock = AsyncMock()

    channel.declare_exchange.return_value = exchange_mock
    channel.declare_queue.side_effect = [lv_queue_mock, analysis_queue_mock, ui_queue_mock]

    await provision_topology(channel)

    assert channel.declare_exchange.await_count == 1
    assert channel.declare_queue.await_count == 3
    
    channel.declare_queue.assert_any_await("lv.queue", durable=True)
    channel.declare_queue.assert_any_await("analysis.queue", durable=True)
    channel.declare_queue.assert_any_await("ui.queue", durable=True)

    assert lv_queue_mock.bind.await_count == 1
    assert analysis_queue_mock.bind.await_count == 2
    assert ui_queue_mock.bind.await_count == 4
