.. _views:

Views
-----

Django Paranoia comes with the same decorators as Django:
*require_http_methods*, *require_GET*, *require_POST*, *require_safe*. Use
these the exact same way you would in Django. But instead import them from this
library, for example::

        from django_paranoia.decorators import require_POST

        @require_POST
        def something_sensitive(request, ...):
            ...

This will return a HTTP 405 Not Allowed response as usual. But it will also
send a warning that an attempt to access with something other than a POST was
made.
