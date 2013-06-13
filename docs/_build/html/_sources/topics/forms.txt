.. _forms:

Forms
-----

Instead of using the builtin form libraries, use the *ParanoidForm* and
*ParanoidModelForm*. If you do this, your forms will raise warnings if:

* more keys are submitted than are required. This may not be useful if you've
  got multiple forms in one request.
* less keys are submitted than are required.
* a key or value contains an ascii character less than 32 (but \t\r\n are ok).

For example::

        from django_paranoia.forms import ParanoidForm

        class Scary(ParanoidForm):
           ...

The log will contain the dodgy data.
