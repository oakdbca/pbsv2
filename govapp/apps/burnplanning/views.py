# from django.shortcuts import render
from django.db.models.query import QuerySet
from rest_framework import viewsets

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


class BurnPlanElementView(BaseView):
    """Burn Plan Element page view."""

    model = BurnPlanElement
