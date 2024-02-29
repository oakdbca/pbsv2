from drf_spectacular import utils as drf_utils
from rest_framework import viewsets

from govapp.apps.logs import models, serializers


@drf_utils.extend_schema(tags=["Logs - Communications Logs"])
class CommunicationsLogEntryViewSet(viewsets.ModelViewSet):
    """Communications Log Entry View Set."""

    queryset = models.CommunicationsLogEntry.objects.all()
    serializer_class = serializers.CommunicationsLogEntrySerializer
    filterset_fields = ["content_type", "object_id"]

    def get_serializer_class(self):
        """Return the serializer class."""
        if self.action == "create":
            return serializers.CommunicationsLogCreateEntrySerializer
        return self.serializer_class

    def perform_create(self, serializer):
        communications_log_entry = serializer.save(user=self.request.user)
        # Save the files
        for f in self.request.FILES.getlist("files"):
            document = models.CommunicationsLogDocument()
            document.entry = communications_log_entry
            document.name = str(f)
            document._file = f
            document.save()
        return communications_log_entry


@drf_utils.extend_schema(tags=["Logs - Action Logs"])
class ActionsLogEntryViewSet(viewsets.ModelViewSet):
    """Actions Log Entry View Set."""

    queryset = models.ActionsLogEntry.objects.all()
    serializer_class = serializers.ActionsLogEntrySerializer
    filterset_fields = ["content_type", "object_id"]
