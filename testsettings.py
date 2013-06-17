DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': ':memory:',
    },
}
CACHES = {
    'default': {
        'BACKEND': 'django.core.cache.backends.locmem.LocMemCache',
    }
}

INSTALLED_APPS = ['django.contrib.sessions']
SESSION_ENGINE = 'django_paranoia.sessions'
DJANGO_PARANOIA_REPORTERS = ['django_paranoia.reporters.log']

SECRET_KEY = '<unused>'

ALLOWED_HOSTS = ['testserver']
