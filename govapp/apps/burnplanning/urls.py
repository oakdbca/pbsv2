from django import urls
from rest_framework import routers

from govapp.apps.burnplanning import views
from govapp.views import IndexPage

router = routers.DefaultRouter()
router.register(
    r"burn-plan-elements", views.BurnPlanElementViewSet, basename="burn-plan-elements"
)
router.register(
    r"burn-planning-units", views.BurnPlanUnitViewSet, basename="burn-planning-units"
)
router.register(r"treatments", views.TreatmentViewSet, basename="treatments")
router.register(r"purposes", views.PurposeViewSet, basename="purposes")
router.register(r"programs", views.ProgramViewSet, basename="programs")
router.register(r"status", views.StatusViewSet, basename="status")
router.register(
    r"indicative-treatment-years",
    views.IndicativeTreatmentYearViewSet,
    basename="indicative-treatment-years",
)
router.register(
    r"revised-indicative-treatment-years",
    views.RevisedIndicativeTreatmentYearViewSet,
    basename="revised-indicative-treatment-years",
)


urlpatterns = [
    urls.path("burn-planning", IndexPage.as_view(), name="burn-planning"),
    urls.path(
        "burn-plan-elements/<int:pk>",
        IndexPage.as_view(),
        name="burn-plan-element-detail",
    ),
    urls.path("burn-planning-units", IndexPage.as_view(), name="burn-planning-units"),
    urls.path(
        "burn-plan-units/<int:pk>",
        IndexPage.as_view(),
        name="burn-plan-unit-detail",
    ),
]
