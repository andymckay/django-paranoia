from django.dispatch import Signal

finished = Signal(providing_args=['request'])
process = Signal(providing_args=['type', 'message', 'values', 'request'])
warning = Signal(providing_args=['type', 'message', 'values'])
