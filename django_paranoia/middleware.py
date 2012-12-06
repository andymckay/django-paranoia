from .signals import finished


class Middleware(object):

    def process_response(self, request, response):
        finished.send(sender=self, request=request)
        return response
