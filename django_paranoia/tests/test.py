# -*- coding: utf-8 -*-

from django import forms
from django.conf import settings
minimal = {
    'DATABASES': {
        'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': 'mydatabase'
        }
    },
    'SESSION_ENGINE': 'django_paranoia.sessions'
}

if not settings.configured:
    settings.configure(**minimal)

from django.db import models
from django.http import HttpResponse, HttpResponseNotAllowed
from django.test import TestCase
from django.test.client import RequestFactory

import mock
from nose.tools import eq_, ok_
from django_paranoia.configure import config

from django_paranoia.decorators import require_http_methods
from django_paranoia.forms import ParanoidForm, ParanoidModelForm
from django_paranoia.middleware import Middleware
from django_paranoia.sessions import SessionStore, ParanoidSessionMiddleware
from django_paranoia.signals import finished, warning


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
        self.warning = warning.connect(self.result)
        self.finished = finished.connect(self.result)


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
        eq_(set(res['values']), set(['sql', 'no']))

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

    def test_dodgy_value(self):
        SimpleForm({'yes': chr(6)})
        assert self.called

    def test_dodgy_key(self):
        SimpleForm({chr(6): 'yes'})
        # Once because chr(6) is an extra char, once because of the key.
        eq_(len(self.called), 2)

    def test_dodgy_allowed(self):
        for x in ['\t', '\r', '\n']:
            self.called = []
            SimpleForm({'yes': x})
            assert not self.called

    def test_dody_unicode(self):
        SimpleForm({'yes': u'Һејдәр Әлијев'})
        assert not self.called


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

    def request(self, **kwargs):
        req = RequestFactory().get('/')
        req.META.update(**kwargs)
        return req

    def get(self, request=None, uid=None):
        request = request if request else self.request()
        return SessionStore(request_meta=request.META.copy(),
                            session_key=uid)

    def test_basic(self):
        self.session = self.get()
        self.session['foo'] = 'bar'
        self.session.save()
        eq_(self.get(uid=self.session.session_key).load()['foo'], 'bar')

    def test_request(self):
        session = self.get()
        session.save()
        res = self.get(uid=session.session_key)
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


class TestMiddleware(ResultCase):

    def test_middle(self):
        Middleware().process_response(RequestFactory().get('/'),
                                      HttpResponse())
        args = self.called[0][1]
        ok_('request_meta' in args)
        eq_(args['request_path'], '/')

    def test_paranoia(self):
        middle = ParanoidSessionMiddleware()
        request = RequestFactory().get('/')
        middle.process_request(request)
        request.session['foo'] = 'bar'
        request.session.save()

        # Change the address.
        request.META['REMOTE_ADDR'] = 'foo'
        middle.process_response(request, HttpResponse())
        assert self.called

    @mock.patch.object(settings, 'SESSION_ENGINE',
                       'django_paranoia.tests.fakesessions')
    def test_paranoid_session_must_be_correct_instance(self):
        middle = ParanoidSessionMiddleware()
        request = RequestFactory().get('/')
        with self.assertRaises(ValueError):
            middle.process_request(request)
