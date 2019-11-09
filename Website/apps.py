from django.apps import AppConfig


class WebsiteConfig(AppConfig):
    name = 'Website'

    def ready(self):
        import Website.signals
