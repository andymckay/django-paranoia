from django.forms import Form, ModelForm

from flags import EXTRA_FIELDS, trans
from signals import warning

# Work in progress.
# We aren't trying to be definitive here yet. Just spot stupid things.

class Paranoid(object):

    def __init__(self, data=None, files=None, **kwargs):
        super(Paranoid, self).__init__(data=data, files=files, **kwargs)
        data = data or {}
        extra = [k for k in data if k not in self.fields]
        if extra:
            klass = self.__class__
            msg = (u'%s: %s in %s' %
                   (trans[EXTRA_FIELDS], extra, klass.__name__))
            warning.send(sender=klass, flag=EXTRA_FIELDS,
                         message=msg, values=extra)

    def clean(self):
        result = super(Paranoid, self).clean()
        for k, v in self.cleaned_data.values():
            # Spot SQL injection attempts.
            # Spot XSS attempt.
            pass
        return result


class ParanoidForm(Paranoid, Form):
    pass


class ParanoidModelForm(Paranoid, ModelForm):
    pass
