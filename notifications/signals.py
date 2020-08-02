from django.dispatch import Signal

notify = Signal(providing_args=['receipient', 'verb', 'action', 'target', 'affected_users'])
