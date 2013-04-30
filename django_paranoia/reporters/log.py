import logging

log = logging.getLogger('paranoia')


def report(signal, message=None, flag=None, sender=None, values=None,
           request_path=None, request_meta=None, **kwargs):
    log.warning(message)
