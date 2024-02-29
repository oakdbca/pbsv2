from django import urls
from django.conf import settings
from rest_framework import routers

from govapp.apps.main import views

router = routers.DefaultRouter()
if settings.DEBUG is not True:
    router.include_root_view = False

router.register(r"regions", views.RegionViewSet, basename="regions")
router.register(r"districts", views.DistrictViewSet, basename="districts")

urlpatterns = [
    urls.path(
        "api/assign-to-me/",
        views.AssignToMeAPIView.as_view(),
        name="assign-to-me",
    ),
    urls.path(
        "api/assignable-users/",
        views.AssignableUsersAPIView.as_view(),
        name="assignable-users",
    ),
    urls.path(
        "api/assign-to/",
        views.AssignToAPIView.as_view(),
        name="assign-to",
    ),
]
