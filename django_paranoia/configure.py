import logging

from django.utils.importlib import import_module

from signals import warning

log = logging.getLogger('paranoia')


def config(reporters=None, *args, **kw):
    if not reporters:
        try:
            from django.conf import settings
            reporters = getattr(settings, 'DJANGO_PARANOIA_REPORTERS', [])
        except ImportError:
            # This can occur when running the tests, because at this time
            # the settings module isn't created. TODO: fix this.
            return

    for reporter in reporters:
        try:
            to = import_module(reporter).report
        except ImportError:
            log.error('Failed to register the reporter: %s' % reporter)
            continue

        warning.connect(to, dispatch_uid='django-paranoia-%s' % reporter)
