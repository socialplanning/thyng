from django.apps import AppConfig

class MyAppConfig(AppConfig):
    name = 'thyng'
    verbose_name = 'Thyng'

    def ready(self):
        import thyng.signals
