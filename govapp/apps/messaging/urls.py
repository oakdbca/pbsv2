from rest_framework import routers

from govapp.apps.messaging import views

router = routers.DefaultRouter()
router.register("message-batches", views.MessageBatchViewSet)
router.register("messages", views.MessageViewSet)
