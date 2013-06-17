from django.contrib.sessions.backends.cache import SessionStore as Base


class SessionStore(Base):
    """
    Fake session store to swap out with the paranoid session store.
    """
    def __init__(self, *a, **kw):
        pass
