from django.apps import AppConfig


class LegalApprovalConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "govapp.apps.legalapproval"
    verbose_name = "Legal/Approval"

    def ready(self) -> None:
        from django.db.models import CharField
        from django.db.models.functions import Length

        CharField.register_lookup(Length, "length")
