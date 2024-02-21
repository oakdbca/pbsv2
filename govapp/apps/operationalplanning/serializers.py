# Third-Party
from rest_framework import serializers

from govapp.apps.main.serializer import ContentTypeModelSerializer
from govapp.apps.operationalplanning.models import OperationalPlan


class OperationalPlanSerializer(ContentTypeModelSerializer):

    class Meta:
        model = OperationalPlan
        fields = "__all__"


class OperationalPlanDatatableSerializer(serializers.ModelSerializer):
    year = serializers.CharField()
    districts = serializers.ReadOnlyField()
    regions = serializers.ReadOnlyField()
    assigned_to_name = serializers.ReadOnlyField()

    class Meta:
        model = OperationalPlan
        fields = [
            "id",
            "name",
            "burn_plan_unit",
            "year",
            "regions",
            "districts",
            "status",
            "assigned_to_name",
        ]
