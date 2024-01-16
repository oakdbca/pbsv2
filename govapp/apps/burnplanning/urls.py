from django import urls

from govapp.apps.burnplanning import views

urlpatterns = [
    urls.path(
        "api/burn-plan-element/<int:pk>/",
        views.BurnPlanElementViewSet.as_view({"get": "list"}),
        name="burn-plan-element",
    ),
    urls.path(
        "api/burn-plan-elements/",
        views.BurnPlanElementViewSet.as_view({"get": "list"}),
        name="burn-plan-elements",
    ),
]
