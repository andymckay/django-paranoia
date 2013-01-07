import re

from django.forms import Form, ModelForm

from flags import EXTRA_FIELDS, MISSING_FIELDS, UNEXPECTED_CHARACTER, trans
from signals import warning

# Spot chars below 32, but allow, \t (9), \r (13) and \n (10).
chars = range(0, 9) + range(11, 13) + range(14, 32)
low_chars = re.compile('|'.join(map(chr, chars)))


class Paranoid(object):

    def __init__(self, data=None, files=None, **kwargs):
        super(Paranoid, self).__init__(data=data, files=files, **kwargs)
        # We need to check for extra data when the form is created.
        data = data or {}
        extra = [k for k in data if k not in self.fields]
        if extra:
            self.warn(EXTRA_FIELDS, extra)

        for k, v in data.items():
            # This assumes all binary data is going through FILES which
            # are not covered by django-paranoia. There really shouldn't
            # be any binary data here at all right?
            self.detect_low(k)
            self.detect_low(v)

    def detect_low(self, data):
        if not isinstance(data, basestring):
            return

        if low_chars.search(data):
            warning.send(sender=self.__class__,
                         flag=UNEXPECTED_CHARACTER,
                         message='Unexpected characters')
            # Not sure if we should send through the data in the message.
            # Would that be bad?

    def warn(self, flag, data):
        klass = self.__class__
        msg = (u'%s: %s in %s' % (trans[flag], data, klass.__name__))
        warning.send(sender=klass, flag=flag, message=msg, values=data)

    def is_valid(self):
        # We can't tell what is missing until the end.
        result = super(Paranoid, self).is_valid()
        missing = []
        if not result:
            for k, errors in self.errors.items():
                field = self.fields.get(k)
                for error in errors:
                    if field and error == field.error_messages['required']:
                        missing.append(k)
                    else:
                        missing.append(k)

        if missing:
            self.warn(MISSING_FIELDS, missing)

        return result


class ParanoidForm(Paranoid, Form):
    pass


class ParanoidModelForm(Paranoid, ModelForm):
    pass
