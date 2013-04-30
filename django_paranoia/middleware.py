from .signals import finished


class Middleware(object):

    def process_response(self, request, response):
        finished.send(sender=self, request_path=request.build_absolute_uri(),
                      request_meta=request.META.copy())
        return response
