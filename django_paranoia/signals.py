from django.dispatch import Signal

# These are used internally to hook up to the request finished signal.
finished = Signal(providing_args=['request'])
process = Signal(providing_args=['type', 'message', 'values', 'request'])

# This is the signal that you hook the warnings in the code up to.
warning = Signal(providing_args=['type', 'message', 'values'])
