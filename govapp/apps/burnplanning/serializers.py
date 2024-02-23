from rest_framework import serializers

from govapp.apps.main.serializers import (
    DistrictSerializer,
    GenericKeyValueSerializer,
    RegionSerializer,
)

from .models import BurnPlanElement, Program, Purpose, Treatment


class PurposeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Purpose
        fields = "__all__"


class ProgramSerializer(serializers.ModelSerializer):
    class Meta:
        model = Program
        fields = "__all__"


class BurnPlanElementSerializer(serializers.ModelSerializer):
    regions = serializers.SerializerMethodField()
    districts = serializers.SerializerMethodField()
    treatment = serializers.CharField(source="treatment.name", read_only=True)
    purposes = PurposeSerializer(many=True, read_only=True)
    programs = ProgramSerializer(many=True, read_only=True)

    class Meta:
        model = BurnPlanElement
        fields = "__all__"

    def get_districts(self, obj):
        return DistrictSerializer(obj.districts, many=True).data

    def get_regions(self, obj):
        return RegionSerializer(obj.regions, many=True).data


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
