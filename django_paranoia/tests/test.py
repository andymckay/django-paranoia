import uuid

from django.conf import settings

minimal = {
    'DATABASES': {
        'default': {
            'ENGINE': 'django.db.backends.sqlite3',
            'NAME': 'mydatabase'
        }
    },
    'CACHES': {
        'default': {
            'BACKEND': 'django.core.cache.backends.locmem.LocMemCache',
        }
    },
    'INSTALLED_APPS': ['django.contrib.sessions'],
    'DJANGO_PARANOIA_REPORTERS': ['django_paranoia.reporters.log'],
}

if not settings.configured:
    settings.configure(**minimal)

from django import forms
from django.db import models
from django.http import HttpResponseNotAllowed
from django.test import TestCase
from django.test.client import RequestFactory

import mock
from nose.tools import eq_
from django_paranoia.configure import config
from django_paranoia.decorators import require_http_methods, require_GET
from django_paranoia.forms import ParanoidForm, ParanoidModelForm
from django_paranoia.sessions import SessionStore
from django_paranoia.signals import warning


class SimpleForm(ParanoidForm):
    yes = forms.BooleanField()


class SimpleModel(models.Model):
    yes = models.BooleanField()


class RequiredForm(SimpleForm):
    req = forms.CharField(required=True)


class SimpleModelForm(ParanoidModelForm):

    class Meta:
        model = SimpleModel


class ResultCase(TestCase):

    def result(self, *args, **kwargs):
        self.called.append((args, kwargs))

    def setUp(self):
        self.called = []
        self.connect = warning.connect(self.result)


class TestForms(ResultCase):

    def test_fine(self):
        SimpleForm()
        SimpleForm({'yes': True})
        assert not self.called

    def test_extra(self):
        SimpleForm({'no': 'wat'})
        assert self.called

    def test_multiple(self):
        SimpleForm({'no': 'wat', 'yes': True, 'sql': 'aargh'})
        res = self.called[0][1]
        eq_(res['values'], ['sql', 'no'])

    def test_model_fine(self):
        SimpleModelForm()
        SimpleModelForm({'yes': True})
        assert not self.called

    def test_model_extra(self):
        SimpleModelForm({'no': 'wat'})
        assert self.called

    def test_required(self):
        form = RequiredForm({})
        assert not form.is_valid()
        res = self.called[0][1]
        eq_(set(res['values']), set(['req', 'yes']))


@mock.patch('django_paranoia.configure.warning')
class TestSetup(TestCase):
    log = 'django_paranoia.reporters.log'

    def test_setup_fails(self, warning):
        config([self.log, 'foo'])
        eq_(len(warning.connect.call_args_list), 1)
        eq_(warning.connect.call_args[1]['dispatch_uid'],
            'paranoia.warning')


class TestLog(TestCase):
    # Not sure what to test here.
    pass


class TestSession(ResultCase):

    def setUp(self):
        self.session = None
        self.uid = 'some:uid'
        super(TestSession, self).setUp()

    def request(self, **kwargs):
        req = RequestFactory().get('/')
        req.META.update(**kwargs)
        return req

    def get(self, request=None):
        session = SessionStore(request=request or self.request(),
                               session_key=self.uid)
        self.uid = session._session_key
        return session

    def save(self):
        self.session.save()

    def test_basic(self):
        self.session = self.get()
        self.session['foo'] = 'bar'
        self.save()
        eq_(self.get().load()['foo'], 'bar')

    def test_request(self):
        self.get().save()
        res = self.get()
        eq_(set(res.request_data().keys()),
            set(['meta:REMOTE_ADDR', 'meta:HTTP_USER_AGENT']))
        assert not self.called

    def test_request_changed(self):
        ses = self.get()
        ses.save()
        req = self.request(REMOTE_ADDR='192.168.1.1')
        ses.check_request_data(request=req)
        assert self.called

    def test_user_agent_changed(self):
        ses = self.get(self.request(HTTP_USER_AGENT='foo'))
        ses.save()
        req = self.request(HTTP_USER_AGENT='bar')
        ses.check_request_data(request=req)
        assert self.called


@require_http_methods(['POST'])
def some(request):
    return True


class TestDecorators(ResultCase):

    def test_some_ok(self):
        assert some(RequestFactory().post('/'))
        assert not self.called

    def test_some_not(self):
        assert isinstance(some(RequestFactory().get('/')),
                          HttpResponseNotAllowed)
        assert self.called
