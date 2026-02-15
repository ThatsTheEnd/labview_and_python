"""Analysis entrypoint."""

from __future__ import annotations

import asyncio
import logging
import signal
import sys

from shared import get_rabbitmq_url

from .service import AnalysisService

logging.basicConfig(
    level=logging.INFO,
    format="[%(asctime)s] %(name)s - %(levelname)s - %(message)s",
)

logger = logging.getLogger(__name__)


def main() -> int:
    service = AnalysisService(get_rabbitmq_url())
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)

    def signal_handler(sig: int, frame: object) -> None:
        logger.info("Received signal %d, shutting down", sig)
        service.should_shutdown = True

    signal.signal(signal.SIGINT, signal_handler)
    signal.signal(signal.SIGTERM, signal_handler)

    try:
        loop.run_until_complete(service.run())
    except Exception:
        logger.exception("Analysis failed")
        return 1
    finally:
        loop.close()

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
