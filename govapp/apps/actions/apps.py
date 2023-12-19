from django.apps import AppConfig


class ActionsConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "govapp.apps.actions"
    verbose_name = "Actions"

    def ready(self) -> None:
        from django.db.models import CharField
        from django.db.models.functions import Length

        CharField.register_lookup(Length, "length")
