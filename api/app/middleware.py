from fastapi import Request, Response
from starlette.middleware.base import BaseHTTPMiddleware, RequestResponseEndpoint
import logging


# Configure logging
logging.basicConfig(level=logging.INFO)


class LoggingMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next: RequestResponseEndpoint) -> Response:
        # Skipping certain logs
        exclude = ('v1/docs', 'v1/openapi.json', 'v1/redoc')
        request_url = str(request.url)
        for term in exclude:
            if term in request_url:
                return await call_next(request)

        logger = logging.getLogger(__name__)
        logger.info(f' Received request: {request.method} {request_url}')
        response = await call_next(request)
        redirect_text = ''
        for header in response.raw_headers:
            if header[0].decode('utf-8') == 'location':
                redirect_text = f'Redirected to Url: {header[1].decode("utf-8")}'

        logger.info(f' Sent response status: {response.status_code} {redirect_text}')
        return response

