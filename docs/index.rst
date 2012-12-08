Django Paranoia
==========================================

Django Paranoia is an attempt to implement some of the OWASP Detection Points
as outlined in this document:

https://www.owasp.org/index.php/AppSensor_DetectionPoints

.. image:: http://www.agmweb.ca/files/keep-calm-and-tell-security.png
        :align: right

Basically it's an attempt to find out when someone is trying to do something
nasty to your site and log it.

*Note*: this is does not prevent any actions that might cause damage to your
site. All the usual prevention measures must be taken to ensure you are not
susceptible to XSS, SQL injection and so on.

.. toctree::
   :maxdepth: 2

   topics/overview.rst
   topics/sessions.rst
   topics/forms.rst
   topics/views.rst

Indices and tables
==================

* :ref:`genindex`
* :ref:`modindex`
* :ref:`search`
