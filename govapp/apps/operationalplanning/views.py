# Third-Party
from drf_spectacular import utils
from rest_framework import viewsets

from govapp.apps.operationalplanning import serializers
from govapp.apps.operationalplanning.models import OperationalPlan


@utils.extend_schema(tags=["Operational Planning - OperationalPlans"])
class OperationalPlanViewSet(viewsets.ReadOnlyModelViewSet):
    """Operational Plan ViewSet."""

    queryset = OperationalPlan.objects.all()
    serializer_class = serializers.OperationalPlanSerializer
