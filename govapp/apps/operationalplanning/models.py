from logging import getLogger

from django.contrib.gis.db.models import MultiLineStringField, MultiPolygonField
from django.db import models
from model_utils import Choices
from model_utils.models import TimeStampedModel
from protected_media.models import ProtectedFileField

from govapp.apps.burnplanning.models import BurnPlanElement
from govapp.apps.main.models import (
    DisplayNameableModel,
    IntervalFloatField,
    IntervalIntegerField,
    Lga,
    ReferenceableModel,
    UniqueNameableModel,
    YearField,
    file_upload_location,
)
from govapp.apps.risk.models import ContributingFactor, RiskFactor
from govapp.apps.traffic.models import Traffic

logger = getLogger(__name__)


# Let's call the class LegalApproval to not confuse with an Approval model
class LegalApproval(DisplayNameableModel):
    """Burn Program and Operational Plan approvals"""

    objects = models.Manager()

    operationalplanapprovals: "models.Manager[OperationalPlanApproval]"

    # TODO Not sure on this one, but requirement item #72 mentions these three separately
    APPROVAL_TYPES = Choices(
        ("endorsement", "Endorsement"),
        ("approval", "Approval"),
        ("endorsement_or_approval", "Endorsement/Approval"),
    )
    approval_type = models.CharField(
        max_length=255, choices=APPROVAL_TYPES, null=True, blank=True
    )
    # TODO There must be a better term than land_type?
    LAND_TYPES = Choices(
        ("shire", "Shire"),
        ("owner", "Owner"),
        ("other", "Other Lands"),
    )
    land_type = models.CharField(
        max_length=255, choices=LAND_TYPES, null=True, blank=True
    )  # To be added by the system after intersection

    approver: models.CharField = models.CharField(
        max_length=255, null=True, blank=True
    )  # Corporate Executive, Shire, Other Lands, Owner

    has_additional_permissions: models.BooleanField = models.BooleanField(
        default=False
    )  # Whether the user can attach files, texts, or remove the approval

    class Meta:
        verbose_name = "Operational Plan Legal/Approval"
        verbose_name_plural = "Operational Plan Legal/Approvals"

    def __str__(self):
        return f"{self.approver} {self.get_approval_type_display()}"

    @property
    def is_shire_approval(self):
        return self.land_type == "shire"

    @property
    def can_remove_approval(self):
        return self.has_additional_permissions and self.text_remove_justification


class OperationalArea(ReferenceableModel, UniqueNameableModel, TimeStampedModel):
    MODEL_PREFIX = "OA"

    objects = models.Manager()

    burn_plan_element: models.ForeignKey = models.ForeignKey(
        BurnPlanElement,
        null=True,
        blank=True,
        on_delete=models.PROTECT,
        related_name="operational_areas",
    )

    # GIS data
    polygon = MultiPolygonField(blank=True, null=True)
    linestring = MultiLineStringField(blank=True, null=True)
    district = models.ForeignKey(
        "main.District",
        null=True,
        blank=True,
        on_delete=models.PROTECT,
        related_name="operational_areas",
    )

    # Overview
    year = YearField(
        null=True, blank=True
    )  # Year in which the operational area is active/valid?
    operational_area_different_from_bpu_rationale = models.TextField(
        null=True, blank=True
    )
    # Contentious burn is coming from BPE Details section for operational area (not sure it belongs here or in BPE)
    contentious_burn = models.BooleanField(default=False)
    contentious_rationale = models.TextField(null=True, blank=True)

    def __str__(self):
        return f"{self.reference_number} ({self.name})"

    @property
    def region(self):
        if self.region:
            return self.district.region
        return None

    @property
    def area_sqm(self):
        if not self.area:
            logger.warn(f"OperationalArea: {self.id} has no area")
            return None
        return self.area.sq_m

    @property
    def area_ha(self):
        if not self.area:
            logger.warn(f"OperationalArea: {self.id} has no area")
            return None
        return self.area.sq_m / 10000

    def copy(self):
        self.pk = None
        self.save()
        return self


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


class OperationalPlan(ReferenceableModel, UniqueNameableModel, TimeStampedModel):
    MODEL_PREFIX = "OP"

    operationalplanapprovals: "models.Manager[OperationalPlanApproval]"
    operationalplanpurposes: "models.Manager[OperationalPlanPurpose]"
    operationalplanprograms: "models.Manager[OperationalPlanProgram]"
    objectiveandsuccesscriteria: "models.Manager[ObjectiveAndSuccessCriteria]"

    operational_area = models.ForeignKey(
        OperationalArea,
        on_delete=models.CASCADE,
        related_name="operational_plans",
    )

    # Overview
    operation_name = models.CharField(
        max_length=255, null=True, blank=True
    )  # To be copied from Details section for operational area in BPE
    purpose: models.ManyToManyField = models.ManyToManyField(
        "burnplanning.Purpose",
        related_name="operational_plans",
        through="OperationalPlanPurpose",
        through_fields=("operational_plan", "purpose"),
        editable=False,
    )  # Copied from BPE, but editable (multi-select)
    program: models.ManyToManyField = models.ManyToManyField(
        "burnplanning.Program",
        related_name="operational_plans",
        through="OperationalPlanProgram",
        through_fields=("operational_plan", "program"),
        editable=False,
    )  # Copied from BPE, but editable (multi-select)

    OPERATIONS = Choices(
        ("burning", "Burning"),
        ("mechanical", "Stand-alone Mechanical"),
    )
    operation = models.CharField(
        max_length=255,
        choices=OPERATIONS,
        null=False,
        blank=False,
        default="burning",
    )
    operational_intent = models.TextField(null=True, blank=True)

    # Priority
    burn_priority = IntervalIntegerField(
        min_value=1, max_value=10, null=True, blank=True
    )
    WINDOW_OF_OPPORTUNITY_VALUES = Choices(
        ("low", "Low"),
        ("medium", "Medium"),
        ("high", "High"),
    )
    window_of_opportunity = models.CharField(
        max_length=255,
        choices=WINDOW_OF_OPPORTUNITY_VALUES,
        null=True,
        blank=True,
    )  # Chance of completing burn if postponed

    # Context
    context_description_of_burn = models.TextField(
        null=True, blank=True, verbose_name="Description of burn"
    )
    context_risk_of_not_completing_burn = models.TextField(
        null=True, blank=True, verbose_name="Risk of not completing burn"
    )
    context_operational_aspects = models.TextField(
        null=True, blank=True, verbose_name="Operational aspects (PESTLE)"
    )
    context_map = ProtectedFileField(
        upload_to=file_upload_location, null=True, blank=True
    )

    # Objectives and Success Criteria: ObjectiveAndSuccessCriteria

    # Traffic
    traffic = models.ForeignKey(
        Traffic,
        on_delete=models.PROTECT,
        null=True,
        blank=True,
        related_name="operational_plans",
    )

    # Legal / Approvals
    legal_approvals: models.ManyToManyField = models.ManyToManyField(
        LegalApproval,
        related_name="operational_plans",
        through="OperationalPlanApproval",
        through_fields=("operational_plan", "legal_approval"),
        editable=False,
    )
    # Risk Factors: OperationalAreaRiskFactor

    @property
    def risk_highest_level(self):
        # Highest risk level from Risk section
        raise NotImplementedError("TODO")

    @property
    def priority_calculated(self):
        # Calculated priority from Priority section
        raise NotImplementedError("TODO")


class OperationalPlanApproval(TimeStampedModel):
    operational_plan = models.ForeignKey(
        OperationalPlan,
        on_delete=models.CASCADE,
        related_name="operationalplanapprovals",
    )
    legal_approval = models.ForeignKey(
        LegalApproval,
        on_delete=models.CASCADE,
        related_name="operationalplanapprovals",
    )

    lga: models.ForeignKey = models.ForeignKey(
        Lga,
        on_delete=models.PROTECT,
        null=True,
        blank=True,
        verbose_name="Shire/LGA",
        related_name="operationalplanapprovals",
    )  # Shire
    file_as_approval = ProtectedFileField(
        upload_to=file_upload_location, null=True, blank=True
    )
    text_as_approval: models.TextField = models.TextField(null=True, blank=True)
    text_remove_justification: models.TextField = models.TextField(
        null=True, blank=True
    )

    class Meta:
        verbose_name_plural = "Operational Plan Legal/Approvals"
        unique_together = ("operational_plan", "legal_approval")

    def __str__(self):
        return (
            f"Operational Area: {self.operational_plan} "
            f"has legal/approval: {self.legal_approval}"
        )

    @property
    def has_lga(self):
        return self.legal_approval.has_lga

    @property
    def has_additional_permissions(self):
        return self.legal_approval.has_additional_permissions


class OperationalPlanPurpose(TimeStampedModel):
    operational_plan = models.ForeignKey(
        OperationalPlan,
        on_delete=models.CASCADE,
        related_name="operationalplanpurposes",
    )
    purpose = models.ForeignKey(
        "burnplanning.Purpose",
        on_delete=models.CASCADE,
        related_name="operationalplanpurposes",
    )


class OperationalPlanProgram(TimeStampedModel):
    operational_plan = models.ForeignKey(
        OperationalPlan,
        on_delete=models.CASCADE,
        related_name="operationalplanprograms",
    )
    program = models.ForeignKey(
        "burnplanning.Program",
        on_delete=models.CASCADE,
        related_name="operationalplanprograms",
    )


class SuccessCriteriaLeftValue(UniqueNameableModel, DisplayNameableModel):
    class Meta:
        verbose_name = "Objective and Success Criteria - Success Criterion Left Value"
        verbose_name_plural = (
            "Objective and Success Criteria - Success Criterion Left Values"
        )


class SuccessCriteriaComparisonOperator(UniqueNameableModel, DisplayNameableModel):
    class Meta:
        verbose_name = (
            "Objective and Success Criteria - Success Criterion Comparison Operator"
        )
        verbose_name_plural = (
            "Objective and Success Criteria - Success Criterion Comparison Operators"
        )


class SuccessCriteriaReport(UniqueNameableModel, DisplayNameableModel):
    class Meta:
        verbose_name = "Objective and Success Criteria - Success Criterion Report"
        verbose_name_plural = (
            "Objective and Success Criteria - Success Criterion Reports"
        )

    success_criteria = models.ForeignKey(
        "SuccessCriteria",
        on_delete=models.CASCADE,
        related_name="successcriteriareports",
        null=True,
        blank=True,
    )

    RESULTS = Choices(
        ("achieved", "Achieved"),
        ("not_achieved", "Not Achieved"),
        ("not_ started", "Not Started"),
    )
    result = models.CharField(
        max_length=255,
        choices=RESULTS,
        null=True,
        blank=True,
    )
    # Allow for recording a percentage if the result is achieved or not achieved. Modeling this as a ratio [0,1]
    result_achieved_ratio = IntervalFloatField(
        min_value=0.0, max_value=1.0, null=True, blank=True
    )


class SuccessCriteria(UniqueNameableModel, DisplayNameableModel):
    class Meta:
        verbose_name = "Objective and Success Criteria - Success Criterion"
        verbose_name_plural = "Objective and Success Criteria - Success Criteria"

    objectiveandsuccesscriteria: "models.Manager[ObjectiveAndSuccessCriteria]"

    left_value = models.ForeignKey(
        SuccessCriteriaLeftValue,
        on_delete=models.CASCADE,
        related_name="successcriteria",
        null=True,
        blank=True,
    )
    comparison_operator = models.ForeignKey(
        SuccessCriteriaComparisonOperator,
        on_delete=models.CASCADE,
        related_name="successcriteria",
        null=True,
        blank=True,
    )
    right_value_or_free_text = models.TextField(null=True, blank=True)
    objective_and_success_criteria = models.ForeignKey(
        "ObjectiveAndSuccessCriteria",
        on_delete=models.CASCADE,
        related_name="success_criteria",
        null=True,
        blank=True,
    )


class Objective(UniqueNameableModel, DisplayNameableModel):
    class Meta:
        verbose_name = "Objective and Success Criteria - Objective"
        verbose_name_plural = "Objective and Success Criteria - Objectives"

    objectiveandsuccesscriteria: "models.Manager[ObjectiveAndSuccessCriteria]"


class ObjectiveAndSuccessCriteria(TimeStampedModel):
    class Meta:
        verbose_name = "Objective and Success Criterion"
        verbose_name_plural = "Objective and Success Criteria"

    operational_plan = models.ForeignKey(
        OperationalPlan,
        on_delete=models.CASCADE,
        related_name="objectiveandsuccesscriteria",
    )
    objective = models.ForeignKey(
        Objective,
        on_delete=models.CASCADE,
        related_name="objectiveandsuccesscriteria",
    )
    details = models.TextField(null=True, blank=True)
    applicable_to_whole_operational_area = models.BooleanField(default=False)
