"""UI entrypoint."""

from __future__ import annotations

import asyncio
import logging

from nicegui import ui

from shared import get_rabbitmq_url
from ui.dashboard import DemoDashboard
from ui.service import UIService

logging.basicConfig(
    level=logging.INFO,
    format="[%(asctime)s] %(name)s - %(levelname)s - %(message)s",
)

logger = logging.getLogger(__name__)

service = UIService(get_rabbitmq_url())
dashboard = DemoDashboard(service)

async def startup() -> None:
    await service.start()

ui.timer(0.1, startup, once=True)

dashboard.build()

ui.run(title="RabbitMQ Demo", port=8080, reload=False, show=True)
