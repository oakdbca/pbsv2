from django.contrib.auth.models import User
from django.contrib.contenttypes.fields import GenericRelation
from django.db import models
from django.utils import timezone
from model_utils import Choices
from model_utils.models import StatusModel, TimeStampedModel

from govapp.apps.main.models import (
    AssignableModel,
    District,
    ModelFile,
    ReferenceableModel,
    Region,
    UniqueNameableModel,
)


class IgnitionMethod(UniqueNameableModel):
    pass


class AircraftType(UniqueNameableModel):
    pass


class AircraftRegistration(UniqueNameableModel):
    pass


class AviationRequest(
    StatusModel, ReferenceableModel, AssignableModel, TimeStampedModel
):
    MODEL_PREFIX = "AR"
    STATUS = Choices(
        ("draft", "Draft"),
        ("submitted", "Submitted"),
        ("declined", "Declined"),
        ("approved", "Approved"),
    )
    region = models.ForeignKey(
        Region, on_delete=models.PROTECT, null=False, blank=False
    )
    district = models.ForeignKey(
        District, on_delete=models.PROTECT, null=False, blank=False
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
    duration = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        null=False,
        blank=False,
        help_text="The duration in hours (e.g. 1.5)",
    )
    decision_made_by = models.ForeignKey(
        User,
        on_delete=models.PROTECT,
        null=True,
        blank=True,
        related_name="aviation_request_decisions",
    )
    decision_datetime = models.DateTimeField(null=True, blank=True)
    decision_text = models.TextField(null=True, blank=True)
    decision_files = GenericRelation(ModelFile)

    def approve(self, decision_made_by: User, approve_text: str) -> None:
        self.status = self.STATUS.approved
        self.decision_made_by = decision_made_by
        self.decision_datetime = timezone.now()
        self.decision_text = approve_text
        # Todo: Take other actions as required (i.e. email notifications, etc.)
        self.save()

    def decline(self, decision_made_by: User, decline_text: str) -> None:
        self.status = self.STATUS.declined
        self.decision_made_by = decision_made_by
        self.decision_datetime = timezone.now()
        self.decision_text = decline_text
        # Todo: Change related implementation plan status back to draft
        self.save()

    def user_is_assignable(self, user: User) -> tuple[bool, str]:
        # Todo - implement this method
        return super().user_is_assignable(user)
