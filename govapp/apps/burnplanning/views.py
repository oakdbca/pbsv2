# from django.shortcuts import render
from django.db.models.query import QuerySet
from rest_framework import response, viewsets

from govapp.common.views import BaseView

from .models import BurnPlanElement
from .serializers import BurnPlanElementSerializer


class BurnPlanElementViewSet(viewsets.ModelViewSet):
    queryset = BurnPlanElement.objects.none()
    serializer_class = BurnPlanElementSerializer
    # permission_classes = [permissions.IsAuthenticated] # TODO

    def get_queryset(self) -> QuerySet:
        pk = self.kwargs.get("pk", None)
        if pk:
            return BurnPlanElement.objects.filter(pk=pk)
        return BurnPlanElement.objects.all()

    def list(self, request, *args, **kwargs):
        queryset = self.get_queryset()
        serializer = self.serializer_class(queryset, many=True)
        return response.Response({"data": serializer.data})


class BurnPlanElementView(BaseView):
    """Burn Plan Element page view."""

    model = BurnPlanElement
