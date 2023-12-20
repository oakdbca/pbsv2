from django import urls

from govapp.apps.burnplanning import views

urlpatterns = [
    urls.path(
        "api/burn_plan_element/<int:pk>/",
        views.BurnPlanElementViewSet.as_view({"get": "list"}),
        name="burn-plan-element",
    ),
]
