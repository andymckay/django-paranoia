from django.conf import settings
from django.contrib.sessions.middleware import SessionMiddleware
from django.contrib.sessions.backends.cache import SessionStore as Base
from django.core.cache import cache
from django.utils.importlib import import_module

from signals import warning
from flags import trans, SESSION_CHANGED

KEY_PREFIX = 'django_paranoid.sessions:'
DATA_PREFIX = '%sdata' % KEY_PREFIX
META_KEYS = ['REMOTE_ADDR', 'HTTP_USER_AGENT']


class SessionStore(Base):

    def __init__(self, session_key=None, request_meta=None):
        self._cache = cache
        self.request_meta = request_meta
        super(SessionStore, self).__init__(session_key)

    @property
    def cache_key(self):
        return KEY_PREFIX + self._get_or_create_session_key()

    def load(self):
        return super(SessionStore, self).load()

    def prepare_data(self, must_create=False):
        """
        Prepare session data for later inspection.

        This makes a copy of sensitive data so that tampering can be detected.
        """
        data = self._get_session(no_load=must_create)
        data.setdefault(DATA_PREFIX, {})
        if self.request_meta:
            for k in META_KEYS:
                dest = 'meta:%s' % k
                if dest not in data[DATA_PREFIX]:
                    data[DATA_PREFIX][dest] = self.request_meta.get(k, '')

    def save(self, must_create=False):
        self.prepare_data(must_create=must_create)
        return super(SessionStore, self).save(must_create=must_create)

    def request_data(self):
        return self._get_session(no_load=False)[DATA_PREFIX]

    def check_request_data(self, request):
        """
        Inspect session data and warn if it was tampered with.
        """
        data = self._get_session()
        stash = data.get(DATA_PREFIX, None)
        if stash is None:
            # If a subclass overrides save(), this should catch it.
            raise ValueError('Cannot check data because it was not stashed. '
                             'This typically happens in save()')
        for k in META_KEYS:
            saved = stash.get('meta:%s' % k, '')
            current = request.META.get(k, '')
            if saved and saved != current:
                values = [saved, current]
                msg = (u'%s: %s' % (trans[SESSION_CHANGED], values))
                warning.send(sender=self, flag=SESSION_CHANGED,
                             message=msg, values=values)


class ParanoidSessionMiddleware(SessionMiddleware):

    def process_request(self, request):
        engine = import_module(settings.SESSION_ENGINE)
        session_key = request.COOKIES.get(settings.SESSION_COOKIE_NAME, None)
        request.session = engine.SessionStore(request_meta=request.META.copy(),
                                              session_key=session_key)
        if not isinstance(request.session, SessionStore):
            raise ValueError('SESSION_ENGINE session must be an instance of '
                             'django_paranoia.sessions.SessionStore')

    def process_response(self, request, response):
        response = (super(ParanoidSessionMiddleware, self)
                    .process_response(request, response))
        request.session.check_request_data(request)
        return response
