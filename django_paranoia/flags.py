from django.utils.translation import ugettext as _

EXTRA_FIELDS = 'extra-form-fields'  # OWASP: RE6
MISSING_FIELDS = 'missing-form-fields'  # OWASP: RE5
WRONG_METHOD = 'wrong-method'  # OWASP: RE1, RE2, RE3 and RE4
SQL_INJECTION = 'sql-injection-attempt'
SESSION_CHANGED = 'session-changed'
XSS = 'xss-attempt'

trans = {
    EXTRA_FIELDS: _('Attempt to process form with extra values'),
    MISSING_FIELDS: _('Attempt to process form with missing values'),
    SQL_INJECTION: _('Data looks that like SQL injection attempt'),
    SESSION_CHANGED: _('Session data changed'),
    WRONG_METHOD: _('Wrong HTTP method'),
    XSS: _('Data that looks like XSS attempt'),
}

__all__ = [EXTRA_FIELDS, MISSING_FIELDS, SQL_INJECTION,
           SESSION_CHANGED, WRONG_METHOD, XSS]
