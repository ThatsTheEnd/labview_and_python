"""Base RabbitMQ service class for common message handling patterns."""

from __future__ import annotations

import asyncio
import logging
from typing import Any, Callable, Dict

import aio_pika
from aio_pika.abc import AbstractIncomingMessage, AbstractRobustConnection

from .rmq import connect, parse_json, provision_topology, setup_exchange
from .routing import EXCHANGE_NAME, ROUTING_CMD_SHUTDOWN

logger = logging.getLogger(__name__)

# Type alias for message handlers
MessageHandler = Callable[[Dict[str, Any]], Any]


class BaseRabbitMQService:
    """Abstract base class for RabbitMQ-based services.
    
    Provides common lifecycle management and message dispatching for services
    that consume messages from RabbitMQ queues. Subclasses should:
    1. Call super().__init__() with rabbitmq_url and queue_name
    2. Register handlers during __init__() using register_handler()
    3. Optionally override _handle_shutdown() for custom shutdown logic
    """

    def __init__(self, rabbitmq_url: str, queue_name: str) -> None:
        """Initialize the service.

        Args:
            rabbitmq_url: RabbitMQ connection URL
            queue_name: Name of the queue to consume from
        """
        self.rabbitmq_url = rabbitmq_url
        self.queue_name = queue_name
        self.should_shutdown = False
        self.connection: AbstractRobustConnection | None = None
        self.channel: aio_pika.abc.AbstractChannel | None = None
        self.exchange: aio_pika.abc.AbstractExchange | None = None
        self._handlers: Dict[str, MessageHandler] = {}

    def register_handler(self, routing_key: str, handler: MessageHandler) -> None:
        """Register a handler for a routing key.

        Args:
            routing_key: RabbitMQ routing key pattern (e.g., "meas.raw")
            handler: Async callable that accepts a dict payload
        """
        self._handlers[routing_key] = handler

    async def start(self) -> None:
        """Connect to RabbitMQ and start consuming from the queue."""
        logger.info(
            "%s starting, connecting to RabbitMQ at %s",
            self.__class__.__name__,
            self.rabbitmq_url,
        )
        self.connection = await connect(self.rabbitmq_url)
        self.channel = await self.connection.channel()

        await provision_topology(self.channel)

        self.exchange = await setup_exchange(self.channel, EXCHANGE_NAME)

        queue = await self.channel.get_queue(self.queue_name)
        await queue.consume(self._on_message)

        logger.info(
            "%s ready, consuming from %s", self.__class__.__name__, self.queue_name
        )

    async def _on_message(self, message: AbstractIncomingMessage) -> None:
        """Process incoming RabbitMQ message."""
        async with message.process():
            payload = parse_json(message.body)
            routing_key = message.routing_key

            # Dispatch to registered handler
            if routing_key in self._handlers:
                handler = self._handlers[routing_key]
                if asyncio.iscoroutinefunction(handler):
                    await handler(payload)
                else:
                    handler(payload)
            elif routing_key == ROUTING_CMD_SHUTDOWN:
                await self._handle_shutdown(payload)
            else:
                logger.warning("Unknown routing key: %s", routing_key)

    async def _handle_shutdown(self, payload: Dict[str, Any]) -> None:
        """Handle shutdown command. Override in subclass for custom behavior."""
        correlation_id = payload.get("correlation_id", "unknown")
        logger.info(
            "%s received cmd.shutdown: correlation_id=%s, shutting down",
            self.__class__.__name__,
            correlation_id,
        )
        self.should_shutdown = True

    async def run(self) -> None:
        """Start the service and run until shutdown is triggered."""
        await self.start()

        while not self.should_shutdown:
            await asyncio.sleep(1.0)

        await self.stop()

    async def stop(self) -> None:
        """Stop the service and close RabbitMQ connection."""
        logger.info("%s stopping", self.__class__.__name__)
        if self.connection:
            await self.connection.close()
        logger.info("%s stopped", self.__class__.__name__)
