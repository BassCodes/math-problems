from django.apps import AppConfig
from django.core.signals import setting_changed


class ProblemsConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "problems"

    def ready(self):
        import problems.signals
