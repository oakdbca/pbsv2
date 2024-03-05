import logging

from django.urls import reverse
from rest_framework import serializers

from govapp.apps.main.serializer import ContentTypeSerializerMixin
from govapp.apps.main.serializers import (
    DistrictSerializer,
    GenericKeyValueSerializer,
    RegionSerializer,
)

from .models import BurnPlanElement, BurnPlanUnit, Program, Purpose, Treatment

logger = logging.getLogger(__name__)


class PurposeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Purpose
        fields = "__all__"


class ProgramSerializer(serializers.ModelSerializer):
    class Meta:
        model = Program
        fields = "__all__"


class BurnPlanElementSerializer(serializers.ModelSerializer):
    regions = RegionSerializer(many=True)
    districts = DistrictSerializer(many=True)
    treatment = serializers.CharField(
        source="treatment.name", read_only=True, allow_null=True
    )
    purposes = PurposeSerializer(many=True, read_only=True)
    programs = ProgramSerializer(many=True, read_only=True)

    class Meta:
        model = BurnPlanElement
        fields = "__all__"


class BurnPlanElementDatatableSerializer(BurnPlanElementSerializer):
    class Meta:
        model = BurnPlanElement
        fields = "__all__"
        # exclude = (
        #     [] #TODO: Add any fields that are not used in the table so query is faster


class SearchSerializer(ContentTypeSerializerMixin, serializers.Serializer):
    reference_number = serializers.CharField(allow_null=True, required=False)
    name = serializers.CharField(allow_null=True, required=False)
    status = serializers.CharField(allow_null=True, required=False)
    status_display = serializers.CharField(
        source="get_status_display", allow_null=True, required=False
    )
    assigned_to = serializers.CharField(allow_null=True, required=False)

    class Meta:
        model = BurnPlanElement
        fields = [
            "id",
            "reference_number",
            "name",
            "status",
            "status_display",
            "assigned_to",
        ]

    def to_representation(self, instance):
        ret = super().to_representation(instance)
        verbose_name = instance._meta.verbose_name
        viewname = verbose_name.replace(" ", "-").lower() + "-detail"
        ret["link"] = self.context.get("request").build_absolute_uri(
            reverse(viewname, args=[instance.id])
        )
        return ret


class BurnPlanUnitSerializer(serializers.ModelSerializer):
    district_names = serializers.ReadOnlyField()
    regions = serializers.ReadOnlyField()

    class Meta:
        model = BurnPlanUnit
        fields = "__all__"


class BurnPlanUnitDatatableSerializer(BurnPlanUnitSerializer):
    class Meta:
        model = BurnPlanUnit
        fields = "__all__"
        # exclude = (
        #     []
        # )   TODO: Add any fields that are not used in the table so query is faster


class TreatmentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Treatment
        fields = "__all__"


class BurnPlanElementKeyValueModelSerializer(
    serializers.ModelSerializer,
    GenericKeyValueSerializer[serializers.ModelSerializer, BurnPlanElement],
):
    class Meta(GenericKeyValueSerializer.Meta):
        model = BurnPlanElement


class IndicativeTreatmentYearSerializer(BurnPlanElementKeyValueModelSerializer):
    key = serializers.IntegerField(source="indicative_treatment_year")
    value = serializers.IntegerField(source="indicative_treatment_year")


class RevisedIndicativeTreatmentYearSerializer(BurnPlanElementKeyValueModelSerializer):
    key = serializers.IntegerField(source="revised_indicative_treatment_year")
    value = serializers.IntegerField(source="revised_indicative_treatment_year")
