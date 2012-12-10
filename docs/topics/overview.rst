.. _overview:

Overview
--------

Django Paranoia is a library to try and detect nasty things going on your site.
It does not prevent attacks, just logs them.

Setup
=====

To install::

        pip install django-paranoia


Add in the middleware::

        MIDDLEWARE_CLASSES = (
                ...
                'django_paranoia.middleware.Middleware',
        )

Hook up the reporters::

        from django_paranoia import configure
        configure.config([
                'django_paranoia.reporters.log',
        ])

Using
=====

The OWASP Detection points cover a large amount of the Django site, so each
part is covered in seperately:

* :ref:`sessions`
* :ref:`forms`
* :ref:`views`

Output
======

When you configure Django Paranoia, you can pass through a list of reporters.
Current choices are:

* `django_paranoia.reporters.log`: send reports to a log file.
* `django_paranoia.reporters.cef_`: send reports to a CEF log (mostly Mozilla
  specific)
