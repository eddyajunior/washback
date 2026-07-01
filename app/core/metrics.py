from threading import Lock

_metrics = {
    "requests_total": 0,
    "errors_total": 0,
    "total_duration_ms": 0.0,
}

_lock = Lock()


def record_request(status_code: int, duration_ms: float) -> None:
    with _lock:
        _metrics["requests_total"] += 1
        _metrics["total_duration_ms"] += duration_ms

        if status_code >= 400:
            _metrics["errors_total"] += 1


def get_metrics() -> dict:
    with _lock:
        requests_total = _metrics["requests_total"]
        total_duration_ms = _metrics["total_duration_ms"]

        average_duration_ms = (
            round(total_duration_ms / requests_total, 2)
            if requests_total > 0
            else 0
        )

        return {
            "requests_total": requests_total,
            "errors_total": _metrics["errors_total"],
            "average_duration_ms": average_duration_ms,
        }