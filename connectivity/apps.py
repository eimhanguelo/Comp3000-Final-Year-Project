from django.apps import AppConfig


class ConnectivityConfig(AppConfig):
    name = 'connectivity'

    def ready(self):
        import connectivity.signals
