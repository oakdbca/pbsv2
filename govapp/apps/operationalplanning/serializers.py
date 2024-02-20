# Third-Party
from rest_framework import serializers

from govapp.apps.operationalplanning.models import OperationalPlan


class OperationalPlanSerializer(serializers.ModelSerializer):
    class Meta:
        model = OperationalPlan
        fields = "__all__"
