"""Django project views."""


# Third-Party
from django import http
from django import shortcuts
from django.views.generic import base
from django.contrib import auth
from django import conf
from django.core.cache import cache
from owslib.wms import WebMapService
import psycopg2
import json

# Internal
from govapp.apps.accounts import utils

# Typing
from typing import Any

UserModel = auth.get_user_model()


class HomePage(base.TemplateView):
    """Home page view."""

    # Template name
    template_name = "govapp/home.html"

    def get(self, request: http.HttpRequest, *args: Any, **kwargs: Any) -> http.HttpResponse:
        """Provides the GET request endpoint for the HomePage view.

        Args:
            request (http.HttpRequest): The incoming HTTP request.
            *args (Any): Extra positional arguments.
            **kwargs (Any): Extra keyword arguments.

        Returns:
            http.HttpResponse: The rendered template response.
        """
        # Construct Context
        context: dict[str, Any] = {}
        #return http.HttpResponseRedirect('/catalogue/entries/')
        # Render Template and Return
        return shortcuts.render(request, self.template_name, context)

class ManagementCommandsView(base.TemplateView):
    """Home page view."""

    # Template name
    template_name = "govapp/management_commands.html"

    def get(self, request: http.HttpRequest, *args: Any, **kwargs: Any) -> http.HttpResponse:
        # Construct Context
        context: dict[str, Any] = {}

        # Render Template and Return
        return shortcuts.render(request, self.template_name, context)

