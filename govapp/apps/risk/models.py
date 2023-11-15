from logging import getLogger

from django.contrib.postgres.fields import DecimalRangeField
from model_utils.models import TimeStampedModel

from govapp.apps.main.models import UniqueNameableModel

logger = getLogger(__name__)


class StandardControl(UniqueNameableModel, TimeStampedModel):
    pass


class ContributingFactor(UniqueNameableModel, TimeStampedModel):
    factors = DecimalRangeField(default_bounds="[)", blank=True, null=True)  # type: ignore


class RiskCategory(UniqueNameableModel, TimeStampedModel):
    pass
