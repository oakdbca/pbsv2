from logging import getLogger

from django.contrib.postgres.fields import DecimalRangeField
from django.db import models
from model_utils.models import TimeStampedModel

from govapp.apps.main.models import UniqueNameableModel

logger = getLogger(__name__)


class StandardControl(UniqueNameableModel, TimeStampedModel):
    pass


class ContributingFactorStandardControl(models.Model):
    contributing_factor = models.ForeignKey(
        "ContributingFactor",
        on_delete=models.PROTECT,
        related_name="contributing_factor_standard_controls",
    )
    standard_control = models.ForeignKey(
        "StandardControl",
        on_delete=models.PROTECT,
        related_name="contributing_factor_standard_controls",
    )
    revisit_in_implementation_plan = models.BooleanField(default=False)


class ContributingFactor(UniqueNameableModel, TimeStampedModel):
    factors = DecimalRangeField(default_bounds="[)", blank=True, null=True)  # type: ignore
    standard_controls: models.ManyToManyField = models.ManyToManyField(
        StandardControl,
        related_name="contributing_factors",
        through="ContributingFactorStandardControl",
        through_fields=("contributing_factor", "standard_control"),
    )


class RiskCategory(UniqueNameableModel, TimeStampedModel):
    pass
