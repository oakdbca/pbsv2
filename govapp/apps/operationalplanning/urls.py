# Third-Party
from rest_framework import routers

# Local
from govapp.apps.operationalplanning import views

# Router
router = routers.DefaultRouter()
router.register("operational-plans", views.OperationalPlanViewSet)
