from rest_framework import serializers

from .models import BurnPlanElement


class BurnPlanElementSerializer(serializers.ModelSerializer):
    region = serializers.SerializerMethodField()
    district = serializers.SerializerMethodField()

    class Meta:
        model = BurnPlanElement
        fields = "__all__"

    def get_region(self, obj):
        return obj.regions

    def get_district(self, obj):
        return obj.districts
