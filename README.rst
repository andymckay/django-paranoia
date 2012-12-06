A Django lib to expose likely intrusion attempts. Using some of the AppSensor
detection points from OWASP:

https://www.owasp.org/index.php/AppSensor_DetectionPoints

*Note*: this is not really ready for use yet.

Setup
-----

To install::

        pip install django-paranoia


Add in the middleware::

        MIDDLEWARE_CLASSES = (
                ...
                'django_paranoia.middleware.Middleware',
        )

Hook up the reporters in your settings file::

        from django_paranoia import configure
        configure.config([
                'django_paranoia.reporters.log',
                'django_paranoia.reporters.cef_'
        ])
