from logging import getLogger

from django.contrib.postgres.fields import DecimalRangeField
from django.db import models
from model_utils.models import TimeStampedModel

from govapp.apps.main.models import UniqueNameableModel

logger = getLogger(__name__)


class Control(UniqueNameableModel, TimeStampedModel):
    class Meta:
        abstract = True


class StandardControl(Control):
    """Control that can be configured in the admin panel"""

    class Meta:
        verbose_name = "Control (Standard)"
        verbose_name_plural = "Controls (Standard)"


class OverwriteControl(Control):
    """Control to overwrite the default value of a standard control"""

    class Meta:
        verbose_name = "Control (Overwrite)"
        verbose_name_plural = "Controls (Overwrite)"

    standard_control = models.ForeignKey(
        "StandardControl",
        on_delete=models.PROTECT,
        related_name="overwrite_controls",
    )


class ContributingFactorStandardControl(models.Model):
    class Meta:
        unique_together = ("contributing_factor", "standard_control")
        verbose_name = "Standard Control Default Value"
        verbose_name_plural = "Standard Control Default Values"

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
    revisit_in_implementation_plan = models.BooleanField(
        default=False
    )  # Whether control can be revisited in Implementation Plan


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
