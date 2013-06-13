Developers
----------

To run the tests against multiple environments, install `tox`_ using
``pip install tox``. You need at least Python 2.7 to run tox itself but you'll
need 2.6 as well to run all environments. Run the tests like this::

    tox

To run the tests against a single environment::

    tox -e py27-django15

To debug something weird, run tests directly from the virtualenv like::

    .tox/py27-django15/bin/nosetests


.. _tox: http://tox.readthedocs.org/
