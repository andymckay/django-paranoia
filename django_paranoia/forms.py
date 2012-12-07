from django.forms import Form, ModelForm

from flags import EXTRA_FIELDS, MISSING_FIELDS, trans
from signals import warning

# Work in progress.
# We aren't trying to be definitive here yet. Just spot stupid things.

class Paranoid(object):

    def __init__(self, data=None, files=None, **kwargs):
        super(Paranoid, self).__init__(data=data, files=files, **kwargs)
        # We need to check for extra data when the form is created.
        data = data or {}
        extra = [k for k in data if k not in self.fields]
        if extra:
            self.warn(EXTRA_FIELDS, extra)

    def warn(self, flag, data):
        klass = self.__class__
        msg = (u'%s: %s in %s' % (trans[flag], data, klass.__name__))
        warning.send(sender=klass, flag=flag, message=msg, values=data)

    def clean(self):
        result = super(Paranoid, self).clean()
        for k, v in self.cleaned_data.values():
            # Spot SQL injection attempts.
            # Spot XSS attempt.
            pass
        return result

    def is_valid(self):
        # We can't tell what is missing until the end.
        result = super(Paranoid, self).is_valid()
        missing = []
        if not result:
            for k, errors in self.errors.items():
                field = self.fields.get(k)
                for error in errors:
                    if error == field.error_messages['required']:
                        missing.append(k)

        if missing:
            self.warn(MISSING_FIELDS, missing)

        return result


class ParanoidForm(Paranoid, Form):
    pass


class ParanoidModelForm(Paranoid, ModelForm):
    pass
