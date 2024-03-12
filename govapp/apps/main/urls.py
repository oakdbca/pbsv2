from django import urls
from rest_framework import routers

from govapp.apps.main import views

router = routers.DefaultRouter()
router.register(r"search", views.SearchViewSet, basename="search")
router.register(
    r"assigned-items", views.AssignedItemsViewSet, basename="assigned-items"
)
router.register(
    r"items-requiring-endorsement",
    views.EndorsingItemsViewSet,
    basename="items-requiring-endorsement",
)
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
