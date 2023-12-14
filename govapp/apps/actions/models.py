from logging import getLogger

from django.contrib.auth.models import User
from django.contrib.contenttypes.fields import GenericRelation
from django.db import models
from model_utils import Choices
from model_utils.models import StatusModel, TimeStampedModel

from govapp.apps.main.models import ModelFile, UniqueNameableModel

logger = getLogger(__name__)


class ActionResponsibility(UniqueNameableModel):
    actions: "models.Manager[Action]"


class Action(StatusModel, TimeStampedModel):
    STATUS = Choices(("open", "Open"), ("closed", "Closed"))

    CATEGORY_CHOICES = Choices(
        ("pre-treatment", "Pre-treatment"),
        ("day-of-treatment", "Day of treatment"),
        ("post-treatment", "Post-treatment"),
    )  # Timeslot for the action
    category: models.CharField = models.CharField(
        max_length=255, choices=CATEGORY_CHOICES, null=False, blank=False
    )
    action: models.CharField = models.CharField(
        max_length=255, unique=True, null=False, blank=False
    )

    responsibility: models.ForeignKey = models.ForeignKey(
        ActionResponsibility,
        on_delete=models.PROTECT,
        null=True,
        blank=True,
        related_name="actions",
    )
    document = GenericRelation(ModelFile)

    date_created: models.DateField = models.DateField(auto_now_add=True)
    date_closed: models.DateField = models.DateField(null=True, blank=True)
    closed_by: models.ForeignKey = models.ForeignKey(
        User, on_delete=models.PROTECT, null=True, blank=True, related_name="closed_by"
    )
    closed_details: models.TextField = models.TextField(null=True, blank=True)

    due_date_time: models.DateTimeField = models.DateTimeField(null=True, blank=True)
