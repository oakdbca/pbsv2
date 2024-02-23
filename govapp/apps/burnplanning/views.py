# from django.shortcuts import render
from rest_framework import viewsets

from govapp.apps.main.mixins import ChoicesKeyValueListMixin
from govapp.apps.main.views import DjangoFiltersModelViewSet, KeyValueListMixin
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


class BurnPlanElementViewSet(DjangoFiltersModelViewSet):
    queryset = BurnPlanElement.objects.all()
    serializer_class = BurnPlanElementSerializer
    # permission_classes = [permissions.IsAuthenticated] # TODO
    django_filters_filterset_class = BurnPlanElementFilter


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
