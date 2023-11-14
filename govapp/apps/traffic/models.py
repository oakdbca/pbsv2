from django.db import models
from model_utils.models import TimeStampedModel
from protected_media.models import ProtectedFileField

from govapp.apps.main.models import (
    DisplayNameableModel,
    IntervalIntegerField,
    UniqueNameableModel,
    file_upload_location,
)


class Road(UniqueNameableModel, DisplayNameableModel):
    class Meta:
        verbose_name_plural = "Roads"
        ordering = ["name"]

    traffic = models.ForeignKey(
        "Traffic", on_delete=models.PROTECT, null=True, blank=True
    )
    owner = models.CharField(max_length=255, null=True, blank=True)
    speed = IntervalIntegerField(
        min_value=0, max_value=130, null=True, blank=True
    )  # km/h
    shoulder_width = models.FloatField(null=True, blank=True)
    # traffic_guidance_scheme

    def __str__(self):
        return self.name  # Road name


class Traffic(UniqueNameableModel, TimeStampedModel):
    class Meta:
        verbose_name_plural = "Traffic"
        ordering = ["name"]

    indicative_traffic_management_scheme = ProtectedFileField(
        upload_to=file_upload_location, null=True, blank=True
    )  # Attached file will be copied to Traffic section in Implementation Plan

    def __str__(self):
        return self.name
