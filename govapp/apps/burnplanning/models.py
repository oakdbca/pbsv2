from logging import getLogger

from django.conf import settings
from django.contrib.gis.db.models import PolygonField
from django.contrib.gis.db.models.functions import Area
from django.core.validators import MinValueValidator
from django.db import models
from django.db.models.functions import Cast
from model_utils import Choices
from model_utils.models import StatusModel, TimeStampedModel

from govapp.apps.main.models import (
    ArchivableModel,
    AssignableModel,
    District,
    NameableModel,
    ReferenceableModel,
    YearField,
)

logger = getLogger(__name__)


class BurnPlanUnitManager(models.Manager):
    def get_queryset(self):
        return (
            super()
            .get_queryset()
            .annotate(area=Area(Cast("polygon", PolygonField(geography=True))))
        )


class BurnPlanUnit(ReferenceableModel, NameableModel, StatusModel, TimeStampedModel):
    """A burn plan unit is a model to contain geometry information for
    an area that may be assigned to a burn plan element"""

    MODEL_PREFIX = "BPU"

    objects = BurnPlanUnitManager()

    STATUS = Choices(
        ("draft", "Draft"),
        ("current", "Current"),
        ("discarded", "discarded"),
        ("retired", "Retired"),
    )

    district = models.ManyToManyField(
        District,
        through="BurnPlanUnitDistrict",
        through_fields=("burn_plan_unit", "district"),
        editable=False,
    )
    polygon = PolygonField(blank=True, null=True)
    active_from = YearField(null=True, blank=True)
    active_to = YearField(null=True, blank=True)
    allow_recording_of_hectares = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.reference_number} ({self.name})"

    @property
    def area_sqm(self):
        if not self.area:
            logger.warn(f"BurnPlanUnit: {self.id} has no area")
            return None
        return self.area.sq_m

    @property
    def area_sqhm(self):
        if not self.area:
            logger.warn(f"BurnPlanUnit: {self.id} has no area")
            return None
        return self.area.sq_m / 10000


class BurnPlanUnitDistrict(TimeStampedModel):
    """A model to store the relationship between a burn plan unit and a district"""

    burn_plan_unit = models.ForeignKey(BurnPlanUnit, on_delete=models.CASCADE)
    district = models.ForeignKey(District, on_delete=models.CASCADE)
    # Todo: confirm business rules for primary district (largest land area? or other?)
    is_primary = models.BooleanField(default=False)

    def __str__(self):
        return (
            f"Burn Plan Unit: {self.burn_plan_unit} "
            f"includes land in district: {self.district} ({self.district.region})"
        )

    class Meta:
        verbose_name_plural = "Burn Plan Unit Districts"
        unique_together = ("burn_plan_unit", "district")


class Treatment(ReferenceableModel, NameableModel, ArchivableModel, TimeStampedModel):
    pass


class Justification(
    ReferenceableModel, NameableModel, ArchivableModel, TimeStampedModel
):
    pass


class Purpose(ReferenceableModel, NameableModel, ArchivableModel, TimeStampedModel):
    pass


class Program(ReferenceableModel, NameableModel, ArchivableModel, TimeStampedModel):
    pass


class OutputLeaderType(
    ReferenceableModel, NameableModel, ArchivableModel, TimeStampedModel
):
    pass


class OutputLeader(
    ReferenceableModel, NameableModel, ArchivableModel, TimeStampedModel
):
    type = models.ForeignKey(
        OutputLeaderType, on_delete=models.PROTECT, null=True, blank=True
    )
    indicative_treatement_year = YearField(null=True, blank=True)
    revised_indicative_treatment_year = YearField(null=True, blank=True)
    preferred_season = models.CharField(
        max_length=255, choices=settings.SEASON_CHOICES, null=True, blank=True
    )
    comments = models.TextField(null=True, blank=True)


class BurnPlanElement(
    ReferenceableModel, NameableModel, StatusModel, AssignableModel, TimeStampedModel
):
    """A burn plan element is a model to contain information about a burn plan
    element. A burn plan element is a component of a burn plan and may be
    assigned to a burn plan unit"""

    MODEL_PREFIX = "BPE"

    STATUS = Choices(
        ("draft", "Draft"),
        ("current", "Current"),
        ("discarded", "discarded"),
        ("retired", "Retired"),
    )

    year = YearField(null=True, blank=True)
    last_relevant_treatment_year = YearField(null=True, blank=True)
    indicative_treatment_year = YearField(null=True, blank=True)
    revised_indicative_treatment_year = YearField(null=True, blank=True)
    return_interval = models.IntegerField(
        null=True, blank=True, validators=[MinValueValidator(1)]
    )
    preferred_season = models.CharField(
        max_length=255, choices=settings.SEASON_CHOICES, null=True, blank=True
    )
    treatment = models.OneToOneField(
        to=Treatment, on_delete=models.PROTECT, null=True, blank=True
    )
    justification = models.OneToOneField(
        to=Justification, on_delete=models.PROTECT, null=True, blank=True
    )
    purposes = models.ManyToManyField(Purpose)
    programs = models.ManyToManyField(Program)
    output_leaders = models.ManyToManyField("OutputLeader")

    def __str__(self):
        return f"{self.reference_number} ({self.name})"
