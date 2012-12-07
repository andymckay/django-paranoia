from django.utils.translation import ugettext as _

EXTRA_FIELDS = 'extra-form-fields'  # OWASP: RE6
MISSING_FIELDS = 'missing-form-fields'  # OWASP: RE5
WRONG_METHOD = 'wrong-method'  # OWASP: RE1, RE2, RE3 and RE4
SQL_INJECTION = 'sql-injection-attempt'
SESSION_CHANGED = 'session-changed'
UNEXPECTED_CHARACTER = 'unexpected-character'  # RE8
WRONG_METHOD = 'wrong-method'  # OWASP: RE1, RE2, RE3 and RE4
XSS = 'xss-attempt'

trans = {
    EXTRA_FIELDS: _('Attempt to process form with extra values'),
    MISSING_FIELDS: _('Attempt to process form with missing values'),
    SQL_INJECTION: _('Data looks that like SQL injection attempt'),
    SESSION_CHANGED: _('Session data changed'),
    UNEXPECTED_CHARACTER: _('Unexpected character'),
    WRONG_METHOD: _('Wrong HTTP method'),
    XSS: _('Data that looks like XSS attempt'),
}
