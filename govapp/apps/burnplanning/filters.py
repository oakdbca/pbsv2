from django_filters import rest_framework as filters

from .models import BurnPlanElement


class BurnPlanElementFilter(filters.FilterSet):
    treatment = filters.NumberFilter(field_name="treatment_id")
    regions = filters.NumberFilter(
        field_name="burn_plan_unit__districts__region", distinct=True
    )
    districts = filters.NumberFilter(
        field_name="burn_plan_unit__districts", distinct=True
    )

    class Meta:
        model = BurnPlanElement
        fields = [
            "purposes",
            "programs",
            "status",
            "indicative_treatment_year",
            "revised_indicative_treatment_year",
            "regions",
            "districts",
            "treatment",
        ]
