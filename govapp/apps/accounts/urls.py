# Third-Party
from django import urls
from django.views.generic import base
from rest_framework import routers

# Local
from govapp.apps.accounts import views

# Router
router = routers.DefaultRouter()
router.register("users", views.UserViewSet)
router.register("groups", views.GroupViewSet)


# Accounts URL Patterns
urlpatterns = [
    urls.path(
        "profile/",
        base.TemplateView.as_view(template_name="govapp/profile.html"),
        name="profile",
    ),
]
