from django.apps import AppConfig


class ImexAppConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'imex_app'
    def ready(self):
        import imex_app.signals
