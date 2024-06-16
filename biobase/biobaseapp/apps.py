"""Biobaseapp Django application configuration."""
from django.apps import AppConfig


class BiobaseappConfig(AppConfig):
    """
    AppConfig for biobaseapp Django application.

    This class defines the configuration for the biobaseapp Django application.
    It sets the default auto field to BigAutoField and the name to biobaseapp.
    """

    default_auto_field = 'django.db.models.BigAutoField'
    name = 'biobaseapp'
