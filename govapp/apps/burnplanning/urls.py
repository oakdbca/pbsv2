from django import urls
from rest_framework import routers

from govapp.apps.burnplanning import views

router = routers.DefaultRouter()
router.register(
    r"burn-plan-elements", views.BurnPlanElementViewSet, basename="burn-plan-elements"
)
router.register(r"treatments", views.TreatmentViewSet, basename="treatments")
router.register(r"purposes", views.PurposeViewSet, basename="purposes")
router.register(r"programs", views.ProgramViewSet, basename="programs")
router.register(r"status", views.StatusViewSet, basename="status")
router.register(
    r"indicative_treatment_year",
    views.IndicativeTreatmentYearViewSet,
    basename="indicative_treatment_year",
)


urlpatterns = [
    urls.path("api/", urls.include(router.urls)),
    urls.path(
        "burn-plan-elements/<int:pk>/",
        views.BurnPlanElementView.as_view(),
        name="burn-plan-elements",
    ),
]
