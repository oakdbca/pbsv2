# from django.shortcuts import render
from django.db.models.query import QuerySet
from django_filters import rest_framework as filters
from rest_framework import response, viewsets

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
    filter_backends = [filters.DjangoFilterBackend]
    filterset_class = BurnPlanElementFilter

    def get_queryset(self) -> QuerySet:
        pk = self.kwargs.get("pk", None)
        if pk:
            return BurnPlanElement.objects.filter(pk=pk)
        filter = self.filterset_class(self.request.GET, queryset=self.queryset)
        return filter.qs

    def list(self, request, *args, **kwargs):
        queryset = self.get_queryset()
        serializer = self.serializer_class(queryset, many=True)
        return response.Response({"data": serializer.data})


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
