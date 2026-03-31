from django.apps import AppConfig


class MenuConfig(AppConfig):
    name = 'apps.menu'

    def ready(self):
        import apps.menu.signals