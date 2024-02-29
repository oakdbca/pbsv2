# from django.shortcuts import render
from rest_framework import viewsets

from govapp.apps.main.mixins import ChoicesKeyValueListMixin
from govapp.apps.main.models import District, Region
from govapp.apps.main.views import KeyValueListMixin
from govapp.common.views import BaseView

from .filters import BurnPlanElementFilter
from .models import BurnPlanElement, Program, Purpose, Treatment
from .serializers import (
    BurnPlanElementSerializer,
    IndicativeTreatmentYearSerializer,
    ProgramSerializer,
    PurposeSerializer,
    RevisedIndicativeTreatmentYearSerializer,
    TreatmentSerializer,
)


class BurnPlanElementViewSet(viewsets.ModelViewSet):
    queryset = BurnPlanElement.objects.all()
    serializer_class = BurnPlanElementSerializer
    filterset_class = BurnPlanElementFilter

    class Meta:
        datatables_extra_json = ("get_options",)

    def get_options(self):
        return "options", {
            "region": Region.cached_key_value_list(),
            "district": District.cached_key_value_list(),
            "status": BurnPlanElement.STATUS._display_map,
        }


class BurnPlanElementView(BaseView):
    """Burn Plan Element page view"""

    model = BurnPlanElement


class TreatmentViewSet(KeyValueListMixin, viewsets.GenericViewSet):
    """Treatment viewset"""

    queryset = Treatment.objects.all()
    serializer_class = TreatmentSerializer


class PurposeViewSet(KeyValueListMixin, viewsets.GenericViewSet):
    """Purpose viewset"""

    queryset = Purpose.objects.all()
    serializer_class = PurposeSerializer


class ProgramViewSet(KeyValueListMixin, viewsets.GenericViewSet):
    """Program viewset"""

    queryset = Program.objects.all()
    serializer_class = ProgramSerializer


class StatusViewSet(ChoicesKeyValueListMixin, viewsets.GenericViewSet):
    """Status viewset"""

    queryset = BurnPlanElement.objects.none()
    choices_dict = BurnPlanElement.STATUS._display_map


class IndicativeTreatmentYearViewSet(KeyValueListMixin, BurnPlanElementViewSet):
    """Indicative Treatment Year viewset"""

    key_value_display_field = "indicative_treatment_year"
    key_value_serializer_class = IndicativeTreatmentYearSerializer


class RevisedIndicativeTreatmentYearViewSet(KeyValueListMixin, BurnPlanElementViewSet):
    """Revised Indicative Treatment Year viewset"""

    key_value_display_field = "revised_indicative_treatment_year"
    key_value_serializer_class = RevisedIndicativeTreatmentYearSerializer
