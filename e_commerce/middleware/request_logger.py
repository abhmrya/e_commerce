import logging
from datetime import datetime

logger = logging.getLogger(__name__)

def get_client_ip(request):
    """Get real client IP address even behind proxy."""
    x_forwarded_for = request.META.get("HTTP_X_FORWARDED_FOR")
    if x_forwarded_for:
        ip = x_forwarded_for.split(",")[0].strip()
    else:
        ip = request.META.get("REMOTE_ADDR")
    return ip

class RequestLoggerMiddleware:
    """Logs client IP, user agent, and request path for each request."""

    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        ip = get_client_ip(request)
        # ip_addresh=request.META.get('REMOTE_ADDR')
        user_agent = request.META.get("HTTP_USER_AGENT", "")
        path = request.path
        method = request.method

        logger.info(
            f"IP->[{ip}]  time->[{datetime.now()}] methos-> {method} path-> {path} | UA: {user_agent}"
        )

        # Store for later use in views
        request.client_ip = ip
        request.client_user_agent = user_agent

        return self.get_response(request)
