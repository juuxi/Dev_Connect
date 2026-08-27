from django.utils.deprecation import MiddlewareMixin
from time import time
import logging


class LoggingMiddleware(MiddlewareMixin):
    logger = logging.getLogger(__name__)

    def process_request(self, request):
        self.start = time()

    def process_response(self, request, response):
        log_info = 'requesting user: '
        log_info += request.user.username if request.user else 'Anonymous user'
        log_info += f', time to process request: {round(time() - self.start, 5)}s'
        self.logger.info(log_info)
        return response
