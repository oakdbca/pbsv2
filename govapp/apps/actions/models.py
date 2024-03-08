from logging import getLogger

from django.contrib.auth.models import User
from django.contrib.contenttypes.fields import GenericForeignKey, GenericRelation
from django.contrib.contenttypes.models import ContentType
from django.db import models
from model_utils import Choices
from model_utils.models import StatusModel, TimeStampedModel

from govapp.apps.main.models import ModelFile, UniqueNameableModel

logger = getLogger(__name__)


class ActionResponsibility(UniqueNameableModel):
    actions: "models.Manager[Action]"

    class Meta:
        verbose_name = "Action Responsibility"
        verbose_name_plural = "Action Responsibilities"


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

    content_type = models.ForeignKey(
        ContentType,
        on_delete=models.CASCADE,
        related_name="content_type_action",
    )
    object_id = models.PositiveIntegerField()
    content_object = GenericForeignKey("content_type", "object_id")

    def __str__(self) -> str:
        return f"{self.content_object}: {self.action} ({self.category}, Status: {self.status})"
