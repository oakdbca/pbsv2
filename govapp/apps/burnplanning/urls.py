from django import urls
from rest_framework import routers

from govapp.apps.burnplanning import views

router = routers.DefaultRouter()
router.register(
    r"burn-plan-elements", views.BurnPlanElementViewSet, basename="burn-plan-elements"
)

urlpatterns = [
    urls.path(
        "burn-plan-elements/<int:pk>/",
        views.BurnPlanElementView.as_view(),
        name="burn-plan-elements",
    ),
]
