from django import urls
from django.views.generic import base

# Accounts URL Patterns
urlpatterns = [
    urls.path(
        "implementation",
        base.TemplateView.as_view(template_name="govapp/implementation.html"),
        name="implementation",
    ),
]
