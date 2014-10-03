from .signals import finished


class Middleware(object):

    def process_response(self, request, response):
        finished.send(sender=self, request_path=request.path_info,
                      request_meta=request.META.copy())
        return response
