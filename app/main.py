"""Entry point for the AI News Aggregator."""

import argparse
import logging
import signal
import sys
import time
from pathlib import Path

from dotenv import load_dotenv

from app.config import get_settings
from app.database import Base, engine
from app.scheduler import run_all_collectors, send_digest, start_scheduler


def _setup_logging() -> None:
    settings = get_settings()
    logging.basicConfig(
        level=settings.log_level.upper(),
        format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
        handlers=[logging.StreamHandler(sys.stdout)],
    )


def _create_tables() -> None:
    Base.metadata.create_all(bind=engine)


def _shutdown(signum, frame, scheduler) -> None:
    logging.getLogger(__name__).info("Shutting down scheduler")
    scheduler.shutdown()
    sys.exit(0)


def run_scheduler() -> None:
    _setup_logging()
    _create_tables()

    logger = logging.getLogger(__name__)
    logger.info("AI News Aggregator starting")

    scheduler = start_scheduler()

    signal.signal(signal.SIGTERM, lambda signum, frame: _shutdown(signum, frame, scheduler))
    signal.signal(signal.SIGINT, lambda signum, frame: _shutdown(signum, frame, scheduler))

    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        _shutdown(signal.SIGINT, None, scheduler)


def run_collect() -> None:
    _setup_logging()
    _create_tables()
    run_all_collectors()


def run_digest() -> None:
    _setup_logging()
    _create_tables()
    send_digest()


def main() -> None:
    env_path = Path(__file__).resolve().parent.parent / ".env"
    if env_path.exists():
        load_dotenv(env_path)

    parser = argparse.ArgumentParser(description="AI News Aggregator")
    subparsers = parser.add_subparsers(dest="command", required=True)

    subparsers.add_parser("run", help="Run the background scheduler")
    subparsers.add_parser("collect", help="Run collectors once")
    subparsers.add_parser("digest", help="Send the daily digest once")

    args = parser.parse_args()

    if args.command == "run":
        run_scheduler()
    elif args.command == "collect":
        run_collect()
    elif args.command == "digest":
        run_digest()


if __name__ == "__main__":
    main()
