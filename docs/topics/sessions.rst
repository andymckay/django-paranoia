.. _sessions:

Sessions
--------

Change your session backend to use Django Paranoid sessions, which is a wrapper
around the cache session. At this time other session backends are *not*
supported.

To configure::

        SESSION_ENGINE = 'django_paranoia.sessions'

        MIDDLEWARE_CLASSES = (
                ...
                'django_paranoia.sessions.ParanoidSessionMiddleware',
        )


When a session is created it will store the user agent and IP address of the
session. If that changes at any time when the request is accessed, it will log.
It will log each time the session is accessed while it's different.

It's assumed that IP address is allowed to change during a session. The user
agent should not.
