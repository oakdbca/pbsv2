# from django.shortcuts import render
from django.db.models.query import QuerySet
from django_filters import rest_framework as filters
from rest_framework import viewsets
from rest_framework_datatables.django_filters.backends import DatatablesFilterBackend

from govapp.apps.main.views import KeyValueListMixin
from govapp.common.views import BaseView

from .filters import BurnPlanElementFilter
from .models import BurnPlanElement, Program, Purpose, Treatment
from .serializers import (
    BurnPlanElementSerializer,
    ProgramSerializer,
    PurposeSerializer,
    TreatmentSerializer,
)


class BurnPlanElementViewSet(viewsets.ModelViewSet):
    queryset = BurnPlanElement.objects.all()
    serializer_class = BurnPlanElementSerializer
    # permission_classes = [permissions.IsAuthenticated] # TODO
    filter_backends = [DatatablesFilterBackend, filters.DjangoFilterBackend]
    filterset_fields = ["treatment"]

    @property
    def filterset_class(self):
        if self.action in ["list"]:
            return BurnPlanElementFilter
        return None

    def filter_queryset(self, queryset: QuerySet) -> QuerySet:
        if self.filterset_class:
            return self.filterset_class(self.request.GET, queryset=self.queryset).qs
        return super().filter_queryset(queryset)


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
