from django.conf import settings
from django.contrib.sessions.middleware import SessionMiddleware
from django.contrib.sessions.backends.cache import SessionStore as Base
from django.core.cache import cache

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

    def save(self, must_create=False):
        data = self._get_session(no_load=must_create)
        data.setdefault(DATA_PREFIX, {})
        if self.request_meta:
            for k in META_KEYS:
                dest = 'meta:%s' % k
                if dest not in data[DATA_PREFIX]:
                    data[DATA_PREFIX][dest] = self.request_meta.get(k, '')
        return super(SessionStore, self).save(must_create=must_create)

    def request_data(self):
        return self._get_session(no_load=False)[DATA_PREFIX]

    def check_request_data(self, request):
        data = self._get_session()
        for k in META_KEYS:
            saved = data.get(DATA_PREFIX, {}).get('meta:%s' % k, '')
            current = request.META.get(k, '')
            if saved and saved != current:
                values = [saved, current]
                msg = (u'%s: %s' % (trans[SESSION_CHANGED], values))
                warning.send(sender=self, flag=SESSION_CHANGED,
                             message=msg, values=values)


class ParanoidSessionMiddleware(SessionMiddleware):

    def process_request(self, request):
        if settings.SESSION_ENGINE != 'django_paranoia.sessions':
            raise ValueError('SESSION_ENGINE must be django_paranoia.sessions')

        session_key = request.COOKIES.get(settings.SESSION_COOKIE_NAME, None)
        request.session = SessionStore(request_meta=request.META.copy(),
                                       session_key=session_key)

    def process_response(self, request, response):
        response = (super(ParanoidSessionMiddleware, self)
                    .process_response(request, response))
        request.session.check_request_data(request)
        return response
