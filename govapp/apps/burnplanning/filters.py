from django_filters import rest_framework as filters

from .models import BurnPlanElement


class BurnPlanElementFilter(filters.FilterSet):
    treatment = filters.NumberFilter(field_name="treatment_id")

    class Meta:
        model = BurnPlanElement
        fields = ["treatment"]
