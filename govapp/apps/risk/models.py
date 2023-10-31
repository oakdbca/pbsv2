from logging import getLogger

from django.contrib.postgres.fields import DecimalRangeField
from django.db import models
from model_utils.models import TimeStampedModel

from govapp.apps.main.models import UniqueNameableModel

logger = getLogger(__name__)


class ContributingFactor(UniqueNameableModel, TimeStampedModel):
    factors = DecimalRangeField(default_bounds="[]", blank=True, null=True)  # type: ignore


class RiskFactor(UniqueNameableModel, TimeStampedModel):
    name: models.CharField = models.CharField(max_length=255)
    contributing_factor = models.ForeignKey(
        ContributingFactor,
        null=True,
        blank=True,
        on_delete=models.PROTECT,
        related_name="risk_factors",
    )
    values_affected = models.TextField(null=True, blank=True)
