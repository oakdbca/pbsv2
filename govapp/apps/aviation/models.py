from django.db import models
from model_utils import Choices
from model_utils.fields import StatusField
from model_utils.models import TimeStampedModel

from govapp.apps.main.models import AssignableModel, NameableModel, ReferenceableModel


class IgnitionMethod(NameableModel):
    pass


class AircraftType(NameableModel):
    pass


class AircraftRegistration(NameableModel):
    pass


class AviationRequest(ReferenceableModel, AssignableModel, TimeStampedModel):
    STATUS = Choices(
        (0, "draft", "Draft"),
        (1, "submitted", "Submitted"),
        (2, "declined", "Declined"),
        (3, "approved", "Approved"),
    )

    ignition_method = models.ForeignKey(
        IgnitionMethod, on_delete=models.PROTECT, null=False, blank=False
    )
    aircraft_type = models.ForeignKey(
        AircraftType, on_delete=models.PROTECT, null=False, blank=False
    )
    aircraft_registration = models.ForeignKey(
        AircraftRegistration, on_delete=models.PROTECT, null=False, blank=False
    )
    datetime_requested = models.DateTimeField(null=False, blank=False)
    duration = models.DurationField(null=False, blank=False)
    status = StatusField()
