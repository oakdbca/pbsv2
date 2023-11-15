from django.contrib.gis.db.models import PointField
from django.db import models
from model_utils.models import TimeStampedModel
from protected_media.models import ProtectedFileField

from govapp.apps.main.models import (
    DisplayNameableModel,
    IntervalIntegerField,
    UniqueNameableModel,
    file_upload_location,
)


class TrafficGuidanceScheme(UniqueNameableModel, DisplayNameableModel):
    class Meta:
        verbose_name_plural = "Traffic Guidance Schemes"
        ordering = ["name"]

    traffic_required_arrangements: "models.Manager[TrafficRequiredArrangement]"

    active_from = models.DateField(null=True, blank=True)
    active_to = models.DateField(null=True, blank=True)
    hyperlink = models.URLField(null=True, blank=True)

    def __str__(self):
        return f"{self.display_name} ({self.hyperlink})"


class RoadOwner(UniqueNameableModel):
    class Meta:
        verbose_name_plural = "Road Owners"
        ordering = ["name"]

    def __str__(self):
        return self.name


class Road(UniqueNameableModel, DisplayNameableModel):
    class Meta:
        verbose_name_plural = "Roads"
        ordering = ["name"]

    owner = models.ForeignKey(
        "RoadOwner",
        on_delete=models.PROTECT,
        null=True,
        blank=True,
        related_name="roads",
    )  # Single-select dropdown
    speed = IntervalIntegerField(
        min_value=0, max_value=130, null=True, blank=True
    )  # km/h
    shoulder_width = models.FloatField(null=True, blank=True)
    traffic_guidance_scheme = models.ForeignKey(
        "TrafficGuidanceScheme",
        on_delete=models.PROTECT,
        null=True,
        blank=True,
        related_name="roads",
    )  # Single-select dropdown

    def __str__(self):
        return self.display_name  # Road name


class TrafficRequiredArrangement(TimeStampedModel):
    """For recording of the Traffic required arrangements in the Traffic section of the Implementation Plan"""

    class Meta:
        verbose_name_plural = "Traffic Required Arrangements"

    # To drop a pin on a map of the implementation area and surroundings
    map_pin = PointField(null=True, blank=True)
    # To attach a guidance scheme to the pin
    traffic_guidance_scheme = models.ForeignKey(
        "TrafficGuidanceScheme",
        on_delete=models.PROTECT,
        null=True,
        blank=True,
        related_name="traffic_required_arrangements",
    )
    date_of_installation = models.DateField(null=True, blank=True)
    traffic = models.ForeignKey(
        "Traffic",
        on_delete=models.PROTECT,
        null=True,
        blank=True,
        related_name="traffic_required_arrangements",
    )

    def __str__(self):
        if not self.traffic_guidance_scheme:
            return f"({self.date_of_installation})"
        return (
            f"{self.traffic_guidance_scheme.display_name} ({self.date_of_installation})"
        )


class Traffic(UniqueNameableModel, DisplayNameableModel, TimeStampedModel):
    class Meta:
        verbose_name_plural = "Traffic"
        ordering = ["name"]

    traffic_required_arrangements: "models.Manager[TrafficRequiredArrangement]"

    indicative_traffic_management_scheme = ProtectedFileField(
        upload_to=file_upload_location, null=True, blank=True
    )  # Attached file will be copied to Traffic section in Implementation Plan
    roads: models.ManyToManyField = models.ManyToManyField(
        "Road", blank=True, related_name="traffics"
    )

    def __str__(self):
        return self.display_name
