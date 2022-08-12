from time import time
from currency.models import ResponseLog


class SimpleMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response
        # One-time configuration and initialization.

    def __call__(self, request):

        start = time()
        request_method = request.method
        path = request.path
        query_params = request.META['QUERY_STRING']
        ip = request.META['REMOTE_ADDR']

        response = self.get_response(request)

        end = time()
        response_time = end - start
        # print(request_method, path, query_params, ip, response_time)
        log_object = ResponseLog.objects.create(
            response_time=response_time,
            request_method=request_method,
            path=path,
            query_params=query_params,
            ip=ip
        )
        log_object.save()

        return response
