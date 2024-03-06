from django import urls
from django.views.generic import base

# Accounts URL Patterns
urlpatterns = [
    urls.path(
        "aviation",
        base.TemplateView.as_view(template_name="govapp/aviation.html"),
        name="aviation",
    ),
]
