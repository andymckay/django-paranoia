from django.utils.translation import ugettext as _

EXTRA_FIELDS = 'extra-form-fields'
SQL_INJECTION = 'sql-injection-attempt'
XSS = 'xss-attempt'
SESSION_CHANGED = 'session-changed'

trans = {
    EXTRA_FIELDS: _('Attempt to process form with extra values'),
    SQL_INJECTION: _('Data looks that like SQL injection attempt'),
    XSS: _('Data that looks like XSS attempt'),
    SESSION_CHANGED: _('Session data changed'),
}

__all__ = [EXTRA_FIELDS, SQL_INJECTION, XSS]
