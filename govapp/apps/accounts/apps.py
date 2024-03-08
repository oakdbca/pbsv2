# Third-Party
from django import apps
from django.conf import settings


class AccountsConfig(apps.AppConfig):
    """Accounts Application Configuration."""

    default_auto_field = "django.db.models.BigAutoField"
    name = "govapp.apps.accounts"

    def ready(self):
        """Ready the application."""
        from django.contrib import auth

        import govapp.apps.accounts.signals  # noqa: F401

        User = auth.get_user_model()
        User.objects.get_or_create(
            email=settings.DEFAULT_FROM_EMAIL,
            defaults={"username": settings.PROJECT_TITLE, "password": ""},
        )
