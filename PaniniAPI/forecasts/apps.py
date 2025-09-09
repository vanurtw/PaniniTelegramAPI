from django.apps import AppConfig


class ForecastsConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'forecasts'


    def ready(self):
        import forecasts.signals
