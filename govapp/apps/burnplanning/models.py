from logging import getLogger

from django.contrib.gis.db.models import PolygonField
from django.contrib.gis.db.models.functions import Area
from django.core.validators import MinValueValidator
from django.db import models
from django.db.models.functions import Cast
from model_utils import Choices
from model_utils.models import StatusModel, TimeStampedModel

from govapp.apps.main.models import District, NameableModel, ReferenceableModel

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
    active_from = models.IntegerField(
        validators=[MinValueValidator(2023)], null=True, blank=True
    )
    active_to = models.IntegerField(
        validators=[MinValueValidator(2023)], null=True, blank=True
    )
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
