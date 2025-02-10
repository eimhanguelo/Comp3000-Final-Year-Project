from django.apps import AppConfig


class TicketConfig(AppConfig):
    name = 'ticket'

    def ready(self):
        import ticket.signals

# apps.py

from django.apps import AppConfig

class TicketAppConfig(AppConfig):
    name = 'ticket'

    def ready(self):
        import ticket.signals  # Ensure signals are connected
