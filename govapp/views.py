from typing import Any

from django import http, shortcuts
from django.contrib import auth
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.views.generic import base

UserModel = auth.get_user_model()


class HomePage(base.TemplateView):
    template_name = "govapp/home.html"

    def get(
        self, request: http.HttpRequest, *args: Any, **kwargs: Any
    ) -> http.HttpResponse:
        if request.user.is_authenticated:
            self.template_name = "govapp/index.html"

        return shortcuts.render(request, self.template_name, context={})


class IndexPage(base.TemplateView):
    template_name = "govapp/index.html"


class ManagementCommandsView(
    LoginRequiredMixin, UserPassesTestMixin, base.TemplateView
):
    """Home page view."""

    # Template name
    template_name = "govapp/management_commands.html"

    def test_func(self) -> bool | None:
        return self.request.user.is_staff

    def get(
        self, request: http.HttpRequest, *args: Any, **kwargs: Any
    ) -> http.HttpResponse:
        # Construct Context
        context: dict[str, Any] = {}

        # Render Template and Return
        return shortcuts.render(request, self.template_name, context)
