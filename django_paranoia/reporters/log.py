import logging

log = logging.getLogger('paranoia')


def report(signal, message=None, flag=None, sender=None, values=None,
           request=None, **kwargs):
    log.warning(message)
