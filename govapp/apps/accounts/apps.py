# Third-Party
from django import apps
from django.conf import settings


class AccountsConfig(apps.AppConfig):
    """Accounts Application Configuration."""

    default_auto_field = "django.db.models.BigAutoField"
    name = "govapp.apps.accounts"

    def ready(self):
        """Ready the application."""
        import govapp.apps.accounts.signals  # noqa: F401

        # When running collectstatic in the docker build the database is not available
        # so we need to catch the OperationalError and pass
        try:
            from django.contrib import auth
            from django.db.utils import OperationalError

            User = auth.get_user_model()
            User.objects.get_or_create(
                email=settings.DEFAULT_FROM_EMAIL,
                defaults={"username": settings.PROJECT_TITLE, "password": ""},
            )
        except OperationalError:
            pass
