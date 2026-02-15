#!/usr/bin/env python3
"""Launch all demo modules together."""

from __future__ import annotations

import asyncio
import logging
import signal
import sys
from pathlib import Path

logging.basicConfig(
    level=logging.INFO,
    format="[%(asctime)s] %(name)s - %(levelname)s - %(message)s",
)

logger = logging.getLogger(__name__)


async def run_module(name: str, module_path: str) -> None:
    """Run a module as a subprocess."""
    process = await asyncio.create_subprocess_exec(
        sys.executable,
        "-m",
        module_path,
        cwd=Path(__file__).parent,
        stdout=asyncio.subprocess.PIPE,
        stderr=asyncio.subprocess.STDOUT,
    )
    
    logger.info(f"{name} started with PID {process.pid}")
    
    async for line in process.stdout:  # type: ignore
        decoded = line.decode().strip()
        if decoded:
            print(f"[{name}] {decoded}")
    
    await process.wait()
    logger.info(f"{name} exited with code {process.returncode}")


async def main() -> int:
    """Launch all modules concurrently."""
    logger.info("Starting all demo modules...")
    
    tasks = [
        asyncio.create_task(run_module("SIMULATOR", "simulator"), name="simulator"),
        asyncio.create_task(run_module("ANALYSIS", "analysis"), name="analysis"),
        asyncio.create_task(run_module("UI", "ui"), name="ui"),
    ]
    
    def signal_handler(sig: int) -> None:
        logger.info(f"Received signal {sig}, cancelling all tasks...")
        for task in tasks:
            task.cancel()
    
    loop = asyncio.get_event_loop()
    loop.add_signal_handler(signal.SIGINT, lambda: signal_handler(signal.SIGINT))
    loop.add_signal_handler(signal.SIGTERM, lambda: signal_handler(signal.SIGTERM))
    
    try:
        await asyncio.gather(*tasks)
    except asyncio.CancelledError:
        logger.info("All modules stopped")
    
    return 0


if __name__ == "__main__":
    raise SystemExit(asyncio.run(main()))
