import json
from datetime import datetime, timezone
from typing import Any

from app.core.logger import logger


def log_info(event: str, **kwargs: Any) -> None:
    payload = {
        "timestamp": datetime.now(timezone.utc).isoformat(),
        "level": "INFO",
        "event": event,
        **kwargs
    }

    logger.info(json.dumps(payload, ensure_ascii=False))


def log_error(event: str, **kwargs: Any) -> None:
    payload = {
        "timestamp": datetime.now(timezone.utc).isoformat(),
        "level": "ERROR",
        "event": event,
        **kwargs
    }

    logger.error(json.dumps(payload, ensure_ascii=False))