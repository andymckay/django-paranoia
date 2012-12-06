from .signals import finished


class Middleware(object):

    def process_response(self, request, response):
        print 'sending finished!'
        import pdb; pdb.set_trace()
        finished.send(sender=self, request=request)
        print 'sending finished!'
        return response
