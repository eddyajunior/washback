import time

from starlette.middleware.base import BaseHTTPMiddleware

from app.core.structured_log import log_info, log_error
from app.core.metrics import record_request


class LoggingMiddleware(BaseHTTPMiddleware):

    async def dispatch(self, request, call_next):

        request_id = getattr(
            request.state,
            "request_id",
            "unknown"
        )

        start_time = time.time()

        try:
            log_info(
                "http_request",
                request_id=request_id,
                method=request.method,
                path=request.url.path
            )

            response = await call_next(request)

            process_time = round(
                (time.time() - start_time) * 1000,
                2
            )

            record_request(
                response.status_code,
                process_time
            )

            log_info(
                "http_response",
                request_id=request_id,
                method=request.method,
                path=request.url.path,
                status_code=response.status_code,
                duration_ms=process_time
            )

            return response

        except Exception as e:

            process_time = round(
                (time.time() - start_time) * 1000,
                2
            )

            log_error(
                "http_error",
                request_id=request_id,
                method=request.method,
                path=request.url.path,
                duration_ms=process_time,
                error=str(e)
            )

            record_request(
                500,
                process_time
            )

            raise