from logging import getLogger

from django.contrib.contenttypes.fields import GenericRelation
from django.contrib.gis.db.models import MultiLineStringField, MultiPolygonField
from django.db import models
from django.forms import ValidationError
from model_utils import Choices
from model_utils.models import TimeStampedModel

from govapp.apps.burnplanning.models import BurnPlanElement
from govapp.apps.main.models import (
    DisplayNameableModel,
    IntervalFloatField,
    IntervalIntegerField,
    Lga,
    ModelFile,
    ReferenceableModel,
    UniqueNameableModel,
    YearField,
)
from govapp.apps.prescriptiondetails.models import (
    PRESCRIPTION_DETAILS,
    FuelType,
    format_prescription_detail_name,
)
from govapp.apps.risk.models import (
    AdditionalControl,
    ContributingFactor,
    OverwriteControl,
    RiskCategory,
    RiskRating,
)
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
    LAND_TYPE_SHIRE = "shire"
    LAND_TYPES = Choices(
        (LAND_TYPE_SHIRE, "Shire"),
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

    def __str__(self) -> str:
        return f"{self.approver} {self.get_approval_type_display()}"

    @property
    def is_shire_approval(self):
        return self.land_type == self.LAND_TYPE_SHIRE

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

    def __str__(self) -> str:
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


class OperationalPlanRiskCategory(models.Model):
    operational_plan = models.ForeignKey(
        "OperationalPlan", null=True, blank=True, on_delete=models.CASCADE
    )
    risk_category = models.ForeignKey(RiskCategory, on_delete=models.CASCADE)
    contributing_factor: models.ManyToManyField = models.ManyToManyField(
        ContributingFactor,
        related_name="risk_categories",
        editable=False,
        through="OperationalPlanRiskCategoryContributingFactor",
        through_fields=("operational_plan_risk_category", "contributing_factor"),
    )  # For each risk category one or more contributing factors can be selected

    def __str__(self) -> str:
        return f"{self.operational_plan} - {self.risk_category}"


# TODO maybe change this class to end in overwrite control OverwriteControl
class OperationalPlanRiskCategoryContributingFactorOverwriteControl(models.Model):
    class Meta:
        verbose_name = "Standard Control Overwrite"
        verbose_name_plural = "Standard Control Overwrites"
        unique_together = (
            "operational_plan_risk_category_contributing_factor",
            "overwrite_control",
        )

    operational_plan_risk_category_contributing_factor = models.ForeignKey(
        "OperationalPlanRiskCategoryContributingFactor",
        on_delete=models.CASCADE,
        related_name="operational_plan_risk_category_contributing_factor_control_overwrites",
    )
    overwrite_control = models.ForeignKey(
        OverwriteControl,
        on_delete=models.CASCADE,
        related_name="operational_plan_risk_category_contributing_factor_control_overwrites",
    )

    def clean(self):
        standard_controls = (
            self.operational_plan_risk_category_contributing_factor.contributing_factor.standard_controls.all()
        )
        if standard_controls.exists() is False:
            raise ValidationError(
                "Contributing factor has no standard controls to overwrite"
            )
        if standard_controls.contains(self.overwrite_control.standard_control) is False:
            raise ValidationError(
                "Overwrite control must be of the same types as contributing factor's standard controls"
            )
        return super().clean()


class OperationalPlanRiskCategoryContributingFactorAdditionalControl(models.Model):
    class Meta:
        verbose_name = "Additional Control"
        verbose_name_plural = "Additional Controls"
        unique_together = (
            "operational_plan_risk_category_contributing_factor",
            "additional_control",
        )

    operational_plan_risk_category_contributing_factor = models.ForeignKey(
        "OperationalPlanRiskCategoryContributingFactor",
        on_delete=models.CASCADE,
        related_name="operational_plan_risk_category_contributing_factor_additional_control",
    )
    additional_control = models.ForeignKey(
        AdditionalControl,
        on_delete=models.CASCADE,
        related_name="operational_plan_risk_category_contributing_factor_additional_control",
    )

    def __str__(self) -> str:
        return f"{self.operational_plan_risk_category_contributing_factor} - {self.additional_control}"

    def clean(self):
        contributing_factor = self.operational_plan_risk_category_contributing_factor
        if (
            not contributing_factor.standard_control_risk_level_requires_additional_controls
        ):
            risk_rating = (
                self.operational_plan_risk_category_contributing_factor.risk_rating_standard
            )
            raise ValidationError(
                f"Additional controls are not required for this standard control risk rating ({risk_rating})"
            )
        return super().clean()

    @property
    def revisit_in_implementation_plan(self):
        return self.additional_control.revisit_in_implementation_plan


class OperationalPlanRiskCategoryContributingFactor(models.Model):
    operational_plan_risk_category = models.ForeignKey(
        OperationalPlanRiskCategory, on_delete=models.CASCADE
    )
    contributing_factor = models.ForeignKey(
        ContributingFactor, on_delete=models.CASCADE
    )
    values_affected = models.TextField(null=True, blank=True)
    contributing_factor_control_overwrites: models.ManyToManyField = models.ManyToManyField(
        OverwriteControl,
        related_name="operational_plan_risk_category_contributing_factors",
        editable=False,
        through="OperationalPlanRiskCategoryContributingFactorOverwriteControl",
        through_fields=(
            "operational_plan_risk_category_contributing_factor",
            "overwrite_control",
        ),
    )  # In IP the standard control contributing factors can be overwritten if revisit_in_implementation_plan is set
    risk_rating_standard = models.ForeignKey(
        RiskRating,
        null=True,
        blank=True,
        on_delete=models.CASCADE,
        related_name="operational_plan_risk_category_contributing_factors_for_standard_controls",
        verbose_name="Risk rating (after application of standard controls)",
    )  # Risk rating after application of standard controls

    additional_controls: models.ManyToManyField = models.ManyToManyField(
        AdditionalControl,
        related_name="operational_plan_risk_category_contributing_factors",
        through="OperationalPlanRiskCategoryContributingFactorAdditionalControl",
        through_fields=(
            "operational_plan_risk_category_contributing_factor",
            "additional_control",
        ),
        editable=False,
    )  # Only applies if risk level of risk rating requires additional controls

    risk_ratings_additional: models.ManyToManyField = models.ManyToManyField(
        RiskRating,
        related_name="operational_plan_risk_category_contributing_factors",
        through="OperationalPlanRiskCategoryContributingFactorAdditionalControlRiskRating",
        through_fields=(
            "operational_plan_risk_category_contributing_factor",
            "risk_rating",
        ),
        editable=False,
    )  # Risk rating after application of additional controls

    def __str__(self) -> str:
        return f"{self.operational_plan_risk_category} - {self.contributing_factor}"

    @property
    def standard_control_risk_level_requires_additional_controls(self):
        if not self.risk_rating_standard:
            return False
        return self.risk_rating_standard.risk_level.requires_additional_controls


class OperationalPlanRiskCategoryContributingFactorAdditionalControlRiskRating(
    models.Model
):
    class Meta:
        verbose_name = "Risk Rating (after application of additional controls)"
        verbose_name_plural = "Risk Ratings (after application of additional controls)"

    operational_plan_risk_category_contributing_factor = models.ForeignKey(
        OperationalPlanRiskCategoryContributingFactor,
        on_delete=models.CASCADE,
        related_name="operational_plan_risk_category_contributing_factor_risk_ratings",
    )
    risk_rating = models.ForeignKey(
        RiskRating,
        null=True,
        blank=True,
        on_delete=models.CASCADE,
        related_name="operational_plan_risk_category_contributing_factor_risk_ratings",
    )

    def __str__(self) -> str:
        return f"{self.operational_plan_risk_category_contributing_factor} {self.risk_rating}"

    def clean(self):
        contributing_factor = self.operational_plan_risk_category_contributing_factor
        if (
            not contributing_factor.standard_control_risk_level_requires_additional_controls
        ):
            risk_rating = (
                self.operational_plan_risk_category_contributing_factor.risk_rating_standard
            )
            raise ValidationError(
                f"Additional risk ratings are not required for this standard control risk rating ({risk_rating})"
            )
        return super().clean()

    @property
    def requires_additional_controls(self):
        return self.risk_rating.risk_level.requires_additional_controls


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
    context_map = GenericRelation(ModelFile)

    # Objectives and Success Criteria: ObjectiveAndSuccessCriteria

    # Traffic
    traffic = models.ForeignKey(
        Traffic,
        on_delete=models.PROTECT,
        null=True,
        blank=True,
        related_name="operational_plans",
    )

    # Burn Values List
    # TODO Sections, Questions, Actions

    # Risk Categories: OperationalPlanRiskCategory
    # risk_ratings

    # Contingencies
    # contingencies

    prescription = models.ForeignKey(
        "Prescription",
        on_delete=models.CASCADE,
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
    file_as_approval = GenericRelation(ModelFile)
    text_as_approval: models.TextField = models.TextField(null=True, blank=True)
    text_remove_justification: models.TextField = models.TextField(
        null=True, blank=True
    )

    class Meta:
        verbose_name_plural = "Operational Plan Legal/Approvals"
        unique_together = ("operational_plan", "legal_approval")

    def __str__(self) -> str:
        return (
            f"Operational Plan: {self.operational_plan} "
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
        ("not_started", "Not Started"),
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


class ContingencyNeighbour(models.Model):
    contingency = models.ForeignKey(
        "Contingency",
        on_delete=models.CASCADE,
        related_name="contingency_neighbours",
    )
    neighbour = models.ForeignKey(
        "main.Neighbour",
        on_delete=models.CASCADE,
        related_name="contingency_neighbours",
    )

    def __str__(self) -> str:
        return f"{self.contingency} - {self.neighbour}"


class Contingency(UniqueNameableModel, DisplayNameableModel):
    class Meta:
        verbose_name = "Contingency"
        verbose_name_plural = "Contingencies"

    operational_plan = models.ForeignKey(
        OperationalPlan,
        on_delete=models.CASCADE,
        related_name="contingencies",
    )
    suppression_constraints = models.TextField(null=True, blank=True)
    neighbours: models.ManyToManyField = models.ManyToManyField(
        "main.Neighbour",
        related_name="contingencies",
        verbose_name="Neighbouring landowners and significant stakeholders",
        through="ContingencyNeighbour",
        through_fields=("contingency", "neighbour"),
    )

    @property
    def context_map(self):
        return self.operational_plan.context_map


class PrescriptionFuelType(models.Model):
    class Meta:
        verbose_name = "Burning Prescription Fuel Type"
        verbose_name_plural = "Burning Prescription Fuel Types"
        unique_together = ("prescription", "fuel_type")

    prescription = models.ForeignKey(
        "Prescription",
        on_delete=models.CASCADE,
        related_name="prescription_fuel_types",
    )
    fuel_type = models.ForeignKey(
        FuelType,
        on_delete=models.CASCADE,
        related_name="prescription_fuel_types",
    )
    cell_name = models.CharField(
        max_length=255, null=True, blank=True, verbose_name="Cell"
    )
    scorch_height = models.ForeignKey(
        "prescriptiondetails.ScorchHeight",
        on_delete=models.CASCADE,
        related_name="prescription_fuel_types",
        null=True,
        blank=True,
        verbose_name=format_prescription_detail_name("scorch_height"),
    )
    burn_area = models.ForeignKey(
        "prescriptiondetails.BurnArea",
        on_delete=models.CASCADE,
        related_name="prescription_fuel_types",
        null=True,
        blank=True,
        verbose_name=format_prescription_detail_name("burn_area"),
    )
    ros_range = models.ForeignKey(
        "prescriptiondetails.RosRange",
        on_delete=models.CASCADE,
        related_name="prescription_fuel_types",
        null=True,
        blank=True,
        verbose_name=format_prescription_detail_name("ros_range"),
    )
    ffdi_range = models.ForeignKey(
        "prescriptiondetails.FfdiRange",
        on_delete=models.CASCADE,
        related_name="prescription_fuel_types",
        null=True,
        blank=True,
        verbose_name=format_prescription_detail_name("ffdi_range"),
    )
    glc_range = models.ForeignKey(
        "prescriptiondetails.GlcRange",
        on_delete=models.CASCADE,
        related_name="prescription_fuel_types",
        null=True,
        blank=True,
        verbose_name=format_prescription_detail_name("glc_range"),
    )
    gfdi_range = models.ForeignKey(
        "prescriptiondetails.GfdiRange",
        on_delete=models.CASCADE,
        related_name="prescription_fuel_types",
        null=True,
        blank=True,
        verbose_name=format_prescription_detail_name("gfdi_range"),
    )
    temperature_range = models.ForeignKey(
        "prescriptiondetails.TemperatureRange",
        on_delete=models.CASCADE,
        related_name="prescription_fuel_types",
        null=True,
        blank=True,
        verbose_name=format_prescription_detail_name("temperature_range"),
    )
    rh_range = models.ForeignKey(
        "prescriptiondetails.RhRange",
        on_delete=models.CASCADE,
        related_name="prescription_fuel_types",
        null=True,
        blank=True,
        verbose_name=format_prescription_detail_name("rh_range"),
    )
    sdi = models.ForeignKey(
        "prescriptiondetails.Sdi",
        on_delete=models.CASCADE,
        related_name="prescription_fuel_types",
        null=True,
        blank=True,
        verbose_name=format_prescription_detail_name("sdi"),
    )
    smc_range = models.ForeignKey(
        "prescriptiondetails.SmcRange",
        on_delete=models.CASCADE,
        related_name="prescription_fuel_types",
        null=True,
        blank=True,
        verbose_name=format_prescription_detail_name("smc_range"),
    )
    pmc_range = models.ForeignKey(
        "prescriptiondetails.PmcRange",
        on_delete=models.CASCADE,
        related_name="prescription_fuel_types",
        null=True,
        blank=True,
        verbose_name=format_prescription_detail_name("pmc_range"),
    )
    wind_speed_range = models.ForeignKey(
        "prescriptiondetails.WindSpeedRange",
        on_delete=models.CASCADE,
        related_name="prescription_fuel_types",
        null=True,
        blank=True,
        verbose_name=format_prescription_detail_name("wind_speed_range"),
    )
    wind_direction = models.ForeignKey(
        "prescriptiondetails.WindDirection",
        on_delete=models.CASCADE,
        related_name="prescription_fuel_types",
        null=True,
        blank=True,
        verbose_name=format_prescription_detail_name("wind_direction"),
    )

    fuel_assessment_summary = GenericRelation(ModelFile)
    fire_behaviour_calculations = GenericRelation(ModelFile)

    def __str__(self) -> str:
        return f"{self.prescription} - {self.fuel_type}"

    @property
    def applicable_fuel_type_prescription_details(self):
        return self.fuel_type.applicable_fuel_type_prescription_details.all()

    def clean(self):
        attrs = PRESCRIPTION_DETAILS.keys()
        applicable_details = self.applicable_fuel_type_prescription_details.values_list(
            "prescription_detail", flat=True
        )
        set_details = [attr for attr in attrs if getattr(self, attr)]
        if any(detail not in applicable_details for detail in set_details):
            raise ValidationError("Invalid prescription detail for this fuel type")
        return super().clean()

    def save(self, *args, **kwargs):
        self.clean()

        super().save(*args, **kwargs)


class Prescription(models.Model):
    class Meta:
        verbose_name = "Prescription"
        verbose_name_plural = "Prescriptions"

    operational_overview = models.TextField(null=True, blank=True)
    ignition_sequence = models.TextField(null=True, blank=True)
    fuel_types: models.ManyToManyField = models.ManyToManyField(
        FuelType,
        related_name="prescriptions",
        verbose_name="Fuel Types",
        through="PrescriptionFuelType",
        through_fields=("prescription", "fuel_type"),
    )

    def __str__(self) -> str:
        truncate_length = 40
        text = str(self.operational_overview)
        return text[:truncate_length] + ".." if len(text) > truncate_length else text
