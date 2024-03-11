import logging

from rest_framework import serializers

from govapp.apps.main.serializers import (
    ContentTypeSerializerMixin,
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


class BurnPlanUnitSerializer(ContentTypeSerializerMixin, serializers.ModelSerializer):
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
