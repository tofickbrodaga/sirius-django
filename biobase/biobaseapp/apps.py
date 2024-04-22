from django.apps import AppConfig


class BiobaseappConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'biobaseapp'

    def ready(self):
        # Import your models or perform any other initialization tasks here
        from .models import CustomUser
