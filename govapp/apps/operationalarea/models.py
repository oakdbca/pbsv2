from logging import getLogger

from django.contrib.gis.db.models import MultiLineStringField, MultiPolygonField
from django.db import models
from model_utils import Choices
from model_utils.models import TimeStampedModel
from protected_media.models import ProtectedFileField

from govapp.apps.burnplanning.models import BurnPlanUnit
from govapp.apps.main.models import (
    DisplayNameableModel,
    Lga,
    ReferenceableModel,
    UniqueNameableModel,
    file_upload_location,
)
from govapp.apps.risk.models import ContributingFactor, RiskFactor

logger = getLogger(__name__)


# Let's call the class LegalApproval to not confuse with an Approval model
class LegalApproval(DisplayNameableModel):
    """Burn Program and Operational Area approvals"""

    objects = models.Manager()

    operationalareaapprovals: "models.Manager[OperationalAreaApproval]"

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

    class Meta:
        verbose_name = "Operational Area Legal/Approval"
        verbose_name_plural = "Operational Area Legal/Approvals"

    def __str__(self):
        if self.lga:
            return f"{self.approver} {self.APPROVAL_TYPE} {self.lga}"
        return f"{self.approver} {self.APPROVAL_TYPE}"


class OperationalArea(ReferenceableModel, UniqueNameableModel, TimeStampedModel):
    MODEL_PREFIX = "OP"

    objects = models.Manager()

    operationalareaapprovals: "models.Manager[OperationalAreaApproval]"

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
    legal_approvals: models.ManyToManyField = models.ManyToManyField(
        LegalApproval,
        related_name="operational_areas",
        through="OperationalAreaApproval",
        through_fields=("operational_area", "legal_approval"),
        editable=False,
    )
    # Risk Factors: OperationalAreaRiskFactor

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


class OperationalAreaApproval(TimeStampedModel):
    operational_area = models.ForeignKey(
        OperationalArea,
        on_delete=models.CASCADE,
        related_name="operationalareaapprovals",
    )
    legal_approval = models.ForeignKey(
        LegalApproval,
        on_delete=models.CASCADE,
        related_name="operationalareaapprovals",
    )

    class Meta:
        verbose_name_plural = "Operational Area Legal/Approvals"
        unique_together = ("operational_area", "legal_approval")

    def __str__(self):
        return (
            f"Operational Area: {self.operational_area} "
            f"has legal/approval: {self.legal_approval}"
        )


class OperationalAreaRiskFactor(models.Model):
    operational_area = models.ForeignKey(
        OperationalArea, null=True, blank=True, on_delete=models.CASCADE
    )
    risk_factor = models.ForeignKey(RiskFactor, on_delete=models.CASCADE)
    contributing_factor = models.ForeignKey(
        ContributingFactor,
        null=True,
        blank=True,
        on_delete=models.PROTECT,
        related_name="risk_factors",
    )
    values_affected = models.TextField(null=True, blank=True)
