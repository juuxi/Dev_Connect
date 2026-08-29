from time import time
import logging


logger = logging.getLogger(__name__)


class LoggingMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        start_time = time()
        response = self.get_response(request)
        duration = round(time() - start_time, 5)

        log_info = 'requesting user: '
        log_info += request.user.username if request.user else 'Anonymous user'
        log_info += f', time to process request: {duration}s'
        logger.info(log_info)
        return response
