import logging
import time


class SimpleMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response
        # One-time configuration and initialization.

    def __call__(self, request):
        # Code to be executed for each request before
        # the view (and later middleware) are called.

        response = self.get_response(request)
        # Code to be executed for each request/response after
        # the view is called.

        return response


class MetricMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response
        # One-time configuration and initialization.

    def __call__(self, request):
        # Get beginning stats
        start_time = time.perf_counter()

        response = self.get_response(request)

        # Get ending stats
        end_time = time.perf_counter()

        # Calculate stats
        total_time = end_time - start_time

        # Log the results
        logger = logging.getLogger('debug')
        logger.info(f'Total time: {(total_time):.2f}s')
        print(f'Total time: {(total_time):.2f}s')

        return response
