import functools

from django.conf import settings

from cef import log_cef


def report(signal, message=None, flag=None, sender=None, values=None,
           request=None, **kwargs):
    g = functools.partial(getattr, settings)
    severity = g('CEF_DEFAULT_SEVERITY', 5)
    cef_kw = {'msg': message, 'signature': request.get_full_path(),
            'config': {
                'cef.product': g('CEF_PRODUCT', 'paranoia'),
                'cef.vendor': g('CEF_VENDOR', 'Mozilla'),
                'cef.version': g('CEF_VERSION', '0'),
                'cef.device_version': g('CEF_DEVICE_VERSION', '0'),
                'cef.file': g('CEF_FILE', 'syslog'),
            }
        }
    log_cef(message, severity, request.META.copy(), **cef_kw)
