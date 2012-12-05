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

    def __init__(self, request=None, session_key=None):
        self._cache = cache
        self.request = request
        super(SessionStore, self).__init__(session_key)

    @property
    def cache_key(self):
        return KEY_PREFIX + self._get_or_create_session_key()

    def load(self):
        return super(SessionStore, self).load()

    def save(self, must_create=False):
        data = self._get_session(no_load=must_create)
        data.setdefault(DATA_PREFIX, {})
        for k in META_KEYS:
            data[DATA_PREFIX]['meta:%s' % k] = self.request.META.get(k, '')
        return super(SessionStore, self).save(must_create=must_create)

    def create(self):
        # Having Django wildly create new sessions is bizarre. Let's
        # instead ensure they are unique. Maybe.
        pass

    def request_data(self):
        return self._get_session(no_load=False)[DATA_PREFIX]

    def check_request_data(self, request):
        data = self._get_session()
        for k in META_KEYS:
            saved = data[DATA_PREFIX]['meta:%s' % k]
            current = request.META.get(k, '')
            if saved and saved != current:
                values = [saved, current]
                msg = msg = (u'%s: %s' % (trans[SESSION_CHANGED], values))
                warning.send(sender=self, flag=SESSION_CHANGED,
                             message=msg, values=values)


class ParanoidSessionMiddleware(SessionMiddleware):

    def process_request(self, request):
        if settings.SESSION_ENGINE != 'django_paranoia.sessions':
            raise ValueError('SESSION_ENGINE must be django_paranoia.sessions')

        session_key = request.COOKIES.get(settings.SESSION_COOKIE_NAME, None)
        request.session = SessionStore(request=request,
                                       session_key=session_key)
