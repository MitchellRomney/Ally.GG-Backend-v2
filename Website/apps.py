from django.apps import AppConfig


class WebsiteConfig(AppConfig):
    name = 'Website'

    def ready(self):
        print("at ready")
        import Website.signals
