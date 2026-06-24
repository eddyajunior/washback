import time

from starlette.middleware.base import BaseHTTPMiddleware

from app.core.logger import logger


class LoggingMiddleware(BaseHTTPMiddleware):

    # async def dispatch(self, request, call_next):

    #     start_time = time.time()

    #     logger.info(
    #         f"REQUEST | {request.method} {request.url.path}"
    #     )

    #     response = await call_next(request)

    #     process_time = round(
    #         (time.time() - start_time) * 1000,
    #         2
    #     )

    #     logger.info(
    #         f"RESPONSE | {request.method} "
    #         f"{request.url.path} | "
    #         f"Status={response.status_code} | "
    #         f"{process_time}ms"
    #     )

    #     return response

    async def dispatch(self, request, call_next):

        request_id = getattr(
            request.state,
            "request_id",
            "unknown"
        )

        start_time = time.time()

        try:

            logger.info(
                f"REQUEST_ID={request_id} | "
                f"REQUEST | "
                f"{request.method} "
                f"{request.url.path}"
            )

            response = await call_next(request)

            process_time = round(
                (time.time() - start_time) * 1000,
                2
            )

            logger.info(
                f"REQUEST_ID={request_id} | "
                f"RESPONSE | "
                f"{request.method} "
                f"{request.url.path} | "
                f"Status={response.status_code} | "
                f"{process_time}ms"
            )

            return response

        except Exception as e:

            process_time = round(
                (time.time() - start_time) * 1000,
                2
            )

            logger.error(
                f"ERROR | {request.method} "
                f"{request.url.path} | "
                f"{process_time}ms | "
                f"{str(e)}"
            )

            raise