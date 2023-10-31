from logging import getLogger

from django.contrib.gis.db.models import MultiLineStringField, MultiPolygonField
from django.db import models
from model_utils import Choices
from model_utils.models import StatusModel, TimeStampedModel
from protected_media.models import ProtectedFileField

from govapp.apps.burnplanning.models import BurnPlanUnit
from govapp.apps.main.models import (
    Lga,
    ReferenceableModel,
    UniqueNameableModel,
    file_upload_location,
)
from govapp.apps.risk.models import RiskFactor

logger = getLogger(__name__)


class OperationalAreaApproval(TimeStampedModel):
    """Burn Program and Operational Area approvals"""

    # TODO What is the difference between an approval and an endorsement?
    APPROVAL_TYPE = Choices(
        ("approval", "Approval"),
        ("endorsement", "Endorsement"),
    )
    approver: models.CharField = models.CharField(
        max_length=255, null=True, blank=True
    )  # Corporate Executive, Shire, Other Lands, Owner
    lga: models.ForeignKey = models.ForeignKey(
        Lga, on_delete=models.PROTECT, null=True, blank=True
    )  # Shire

    can_provide_evidence: models.BooleanField = models.BooleanField(
        default=False
    )  # Whether the user can attach files, texts, or remove the approval
    file_as_approval = ProtectedFileField(upload_to=file_upload_location)
    text_as_approval: models.TextField = models.TextField(null=True, blank=True)
    text_remove_justification: models.TextField = models.TextField(
        null=True, blank=True
    )

    def __str__(self):
        if self.lga:
            return f"{self.approver} {self.APPROVAL_TYPE} {self.lga}"
        return f"{self.approver} {self.APPROVAL_TYPE}"


class OperationalArea(
    ReferenceableModel, UniqueNameableModel, StatusModel, TimeStampedModel
):
    MODEL_PREFIX = "OP"

    burn_plan_unit: models.ForeignKey = models.ForeignKey(
        BurnPlanUnit,
        null=True,
        blank=True,
        on_delete=models.PROTECT,
        related_name="operational_areas",
    )

    MITIGATION_PURPOSE = Choices(
        ("burning", "Burning"),
        ("mechanical", "Stand-alone Mechanical"),
    )

    # GIS data
    polygon = MultiPolygonField(blank=True, null=True)
    linestring = MultiLineStringField(blank=True, null=True)

    # Details
    operation_name = models.CharField(
        max_length=255, null=True, blank=True
    )  # To be pre-filled with the name of the burn plan unit
    # Purpose and Program come from the BPU?
    burn_priority = models.IntegerField(null=True, blank=True)
    contentious_burn = models.BooleanField(default=False)
    contentious_rationale = models.TextField(null=True, blank=True)
    operational_area_different_from_bpu_rationale = models.TextField(
        null=True, blank=True
    )

    # Legal / Approvals
    approvals: models.ManyToManyField = models.ManyToManyField(
        OperationalAreaApproval, blank=True, related_name="operational_areas"
    )

    # Risk Factors
    risk_factors = models.ManyToManyField(
        RiskFactor, blank=True, related_name="operational_areas"
    )

    def __str__(self):
        return f"{self.reference_number} ({self.name})"

    @property
    def purpose(self):
        if self.burn_plan_unit and self.burn_plan_unit.purposes.exists():
            # TODO How to get the selected purpose?
            return self.burn_plan_unit.purposes.first().purpose
        return None

    @property
    def program(self):
        if self.burn_plan_unit and self.burn_plan_unit.programs.exists():
            # TODO How to get the selected program?
            return self.burn_plan_unit.programs.first().program
        return None
