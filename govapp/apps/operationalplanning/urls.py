# Third-Party
from django import urls
from rest_framework import routers

# Local
from govapp.apps.operationalplanning import views
from govapp.views import IndexPage

# Router
router = routers.DefaultRouter()
router.register("operational-plans", views.OperationalPlanViewSet)

urlpatterns = [
    urls.path("operational-planning", IndexPage.as_view(), name="operational-planning"),
    urls.path(
        "operational-plan/<int:pk>/",
        IndexPage.as_view(),
        name="operational-plans",
    ),
]
