from rest_framework import serializers

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
    region = serializers.SerializerMethodField()
    district = serializers.SerializerMethodField()
    treatment = serializers.CharField(source="treatment.name", read_only=True)
    purposes = PurposeSerializer(many=True, read_only=True)
    programs = ProgramSerializer(many=True, read_only=True)

    class Meta:
        model = BurnPlanElement
        fields = "__all__"

    def get_region(self, obj):
        return obj.regions

    def get_district(self, obj):
        return obj.districts


class TreatmentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Treatment
        fields = "__all__"


class IndicativeTreatmentYearSerializer(serializers.ModelSerializer):
    class Meta:
        model = BurnPlanElement
        fields = ["indicative_treatment_year"]
        read_only_fields = ["indicative_treatment_year"]
