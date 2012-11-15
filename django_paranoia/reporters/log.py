import logging

log = logging.getLogger('paranoia')


def report(signal, message=None, flag=None, sender=None, values=None):
    log.warning(message)
