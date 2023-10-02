from drf_spectacular import utils as drf_utils
from rest_framework import viewsets

from govapp.apps.logs import models, serializers
from govapp.common import mixins


@drf_utils.extend_schema(tags=["Logs - Communications Logs"])
class CommunicationsLogEntryViewSet(
    mixins.ChoicesMixin,
    viewsets.GenericViewSet,
):
    """Communications Log Entry View Set."""

    queryset = models.CommunicationsLogEntry.objects.all()
    serializer_class = serializers.CommunicationsLogEntrySerializer
