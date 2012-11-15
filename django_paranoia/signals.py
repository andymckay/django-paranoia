from django.dispatch import Signal

warning = Signal(providing_args=['type', 'message', 'values'])
