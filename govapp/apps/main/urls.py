# Third-Party
from django import urls

# Local
from govapp.apps.main import views

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
