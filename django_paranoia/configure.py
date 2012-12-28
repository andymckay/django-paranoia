import logging
from threading import local

from django.conf import settings
from django.utils.importlib import import_module

from signals import finished, process, warning

log = logging.getLogger('paranoia')

_locals = local()


def setup():
    if not hasattr(_locals, 'signals'):
        _locals.signals = []
        return True


def add_signal(signal, **kw):
    setup()
    # Let's not pickle the sender.
    kw['sender'] = kw['sender'].__name__
    _locals.signals.append(kw)


def reset(**kw):
    setup()
    _locals.signals = []


def process_signals(signal, **kw):
    # We need to batch up all signals here and then send them when the
    # request is finished. This allows us to pass through the request
    # to the reporters, allowing more detailed logs.
    if setup():
        return

    for data in _locals.signals:
        process.send(request=kw['request'], **data)


def config(*args, **kw):
    try:
        reporters = getattr(settings, 'DJANGO_PARANOIA_REPORTERS', [])
    except ImportError:
        return

    for reporter in reporters:
        try:
            to = import_module(reporter).report
        except ImportError:
            log.error('Failed to register the reporter: %s' % reporter)
            continue

        # Each reporter gets connected to the process signal.
        process.connect(to, dispatch_uid='paranoia.reporter.%s' % reporter)

    # The warning signal is sent by forms, sessions etc when they
    # encounter something.
    warning.connect(add_signal, dispatch_uid='paranoia.warning')
    # The finished signal is sent by the middleware when the request is
    # finished. This then processes all the warning signals built up so far
    # on that request.
    finished.connect(process_signals, dispatch_uid='paranoia.finished')
