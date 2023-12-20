from rest_framework import serializers

from .models import BurnPlanElement


class BurnPlanElementSerializer(serializers.ModelSerializer):
    class Meta:
        model = BurnPlanElement
        fields = (
            "id",
            "name",
        )
