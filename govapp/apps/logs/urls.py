# Third-Party
from rest_framework import routers

# Local
from govapp.apps.logs import views

# Router
router = routers.DefaultRouter()
router.register("actions", views.ActionsLogEntryViewSet)
router.register("communications", views.CommunicationsLogEntryViewSet)
