from django import urls
from django.views.generic import base

# Accounts URL Patterns
urlpatterns = [
    urls.path(
        "treatment",
        base.TemplateView.as_view(template_name="govapp/treatment.html"),
        name="treatment",
    ),
]
