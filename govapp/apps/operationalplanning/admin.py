from logging import getLogger

import nested_admin
from django import forms
from django.contrib import admin
from django.contrib.contenttypes.forms import BaseGenericInlineFormSet
from django.utils.html import format_html, format_html_join

from govapp.apps.legalapproval.models import (
    LegalApproval,
    ModelLegalApproval,
    ModelRequiredApproval,
)
from govapp.apps.main.admin import NestedDeleteRestrictedAdmin
from govapp.apps.main.models import ModelFile
from govapp.apps.risk.models import ContributingFactorStandardControl

from .models import (
    Contingency,
    ContingencyNeighbour,
    Objective,
    ObjectiveAndSuccessCriteria,
    OperationalArea,
    OperationalPlan,
    OperationalPlanProgram,
    OperationalPlanPurpose,
    OperationalPlanRiskCategory,
    OperationalPlanRiskCategoryContributingFactor,
    OperationalPlanRiskCategoryContributingFactorAdditionalControl,
    OperationalPlanRiskCategoryContributingFactorAdditionalControlRiskRating,
    OperationalPlanRiskCategoryContributingFactorOverwriteControl,
    Prescription,
    PrescriptionFuelType,
    SuccessCriteria,
    SuccessCriteriaComparisonOperator,
    SuccessCriteriaLeftValue,
    SuccessCriteriaReport,
)

logger = getLogger(__name__)


class OperationalAreaPurposeInline(nested_admin.NestedTabularInline):
    model = OperationalPlanPurpose
    extra = 0


class OperationalAreaProgramInline(nested_admin.NestedTabularInline):
    model = OperationalPlanProgram
    extra = 0


class SuccessCriteriaReportInline(nested_admin.NestedStackedInline):
    model = SuccessCriteriaReport
    extra = 0
    verbose_name = "Success criterion report"
    verbose_name_plural = "Success criterion reports"

    class Media:
        css = {
            "all": ["admin/class_media/css/inline_fieldsets.css"],
        }

    list_display = (
        "name",
        "display_name",
        "result",
        "result_achieved_ratio",
    )

    fieldsets = (
        (
            "Success criterion report",
            {
                "fields": (
                    (
                        "name",
                        "display_name",
                    ),
                    (
                        "result",
                        "result_achieved_ratio",
                    ),
                ),
                "classes": (
                    "collapse",
                    "less-dominant-style",
                    "nested-inline-flex-container",
                ),
            },
        ),
    )


class OperationalPlanRiskCategoryContributingFactorOverwriteControlInline(
    nested_admin.NestedStackedInline
):
    model = OperationalPlanRiskCategoryContributingFactorOverwriteControl
    extra = 0

    fieldsets = (
        (
            None,
            {
                "fields": (
                    (
                        "operational_plan_risk_category_contributing_factor",
                        "overwrite_control",
                    ),
                ),
                "classes": (
                    "less-dominant-style",
                    "nested-inline-flex-container",
                ),
            },
        ),
    )


class OperationalPlanRiskCategoryContributingFactorAdditionalControlRiskRatingInline(
    nested_admin.NestedStackedInline
):
    model = OperationalPlanRiskCategoryContributingFactorAdditionalControlRiskRating
    extra = 1

    list_display = (
        "operational_plan_risk_category_contributing_factor",
        "risk_rating",
        "requires_additional_controls",
    )

    fieldsets = (
        (
            None,
            {
                "fields": (
                    (
                        "operational_plan_risk_category_contributing_factor",
                        "risk_rating",
                        "requires_additional_controls",
                    ),
                ),
                "classes": (
                    "less-dominant-style",
                    "nested-inline-flex-container",
                ),
            },
        ),
    )

    readonly_fields = ("requires_additional_controls",)


class OperationalPlanRiskCategoryContributingFactorAdditionalControlInline(
    nested_admin.NestedStackedInline
):
    model = OperationalPlanRiskCategoryContributingFactorAdditionalControl
    extra = 1

    list_display = (
        "operational_plan_risk_category_contributing_factor",
        "additional_control",
        "revisit_in_implementation_plan",
    )

    fieldsets = (
        (
            None,
            {
                "fields": (
                    (
                        "operational_plan_risk_category_contributing_factor",
                        "additional_control",
                        "revisit_in_implementation_plan",
                    ),
                ),
                "classes": (
                    "less-dominant-style",
                    "nested-inline-flex-container",
                ),
            },
        ),
    )

    readonly_fields = ("requires_additional_controls", "revisit_in_implementation_plan")


class OperationalPlanRiskCategoryContributingFactorInline(
    nested_admin.NestedStackedInline
):
    model = OperationalPlanRiskCategoryContributingFactor
    extra = 1
    verbose_name = "Contributing factor"
    verbose_name_plural = "Contributing factors"

    class Media:
        css = {
            "all": ["admin/class_media/css/inline_fieldsets.css"],
        }

    list_display = (
        "contributing_factor",
        "values_affected",
        "standard_controls",
        "requires_additional_controls",
        "risk_rating_standard",
        "standard_control_risk_level_requires_additional_controls",
    )

    readonly_fields = (
        "standard_controls",
        "standard_control_risk_level_requires_additional_controls",
    )
    fieldsets = (
        (
            "Contributing factor",
            {
                "fields": (
                    (
                        "contributing_factor",
                        "values_affected",
                    ),
                ),
                "classes": (
                    "collapse",
                    "less-dominant-style",
                    "nested-inline-flex-container",
                ),
            },
        ),
        (
            "Standard controls",
            {
                "fields": (
                    ("standard_controls",),
                    (
                        "risk_rating_standard",
                        "standard_control_risk_level_requires_additional_controls",
                    ),
                ),
                "classes": (
                    "less-dominant-style",
                    "nested-inline-flex-container",
                ),
            },
        ),
    )

    classes = ("less-dominant-style", "nested-inline-flex-container")

    inlines = [
        OperationalPlanRiskCategoryContributingFactorOverwriteControlInline,
        OperationalPlanRiskCategoryContributingFactorAdditionalControlInline,
        OperationalPlanRiskCategoryContributingFactorAdditionalControlRiskRatingInline,
    ]

    def standard_controls(self, obj=None):
        """Return a list of standard controls for the contributing factor for purpose of display."""

        if not obj.contributing_factor_id:
            return ""
        return "\n".join(
            [
                f"{cs.standard_control.name}, can revisit in Implementation Plan: {cs.revisit_in_implementation_plan}"
                for cs in ContributingFactorStandardControl.objects.filter(
                    contributing_factor_id=obj.contributing_factor_id
                ).all()
            ]
        )


class SuccessCriteriaInlineForm(forms.ModelForm):
    class Meta:
        model = SuccessCriteria
        fields = "__all__"
        help_texts = {
            "right_value_or_free_text": "If Objective 'Other' is selected, "
            "only a free-text success criteria will be shown."
        }


class SuccessCriteriaInline(nested_admin.NestedStackedInline):
    model = SuccessCriteria
    extra = 1
    form = SuccessCriteriaInlineForm
    verbose_name = "Success criterion"
    verbose_name_plural = "Success criteria"

    list_display = (
        "name",
        "display_name",
        "left_value",
        "comparison_operator",
        "right_value_or_free_text",
    )

    class Media:
        css = {
            "all": ["admin/class_media/css/inline_fieldsets.css"],
        }

    fieldsets = (
        (
            "Success criterion",
            {
                "fields": (
                    (
                        "name",
                        "display_name",
                    ),
                    (
                        "left_value",
                        "comparison_operator",
                        "right_value_or_free_text",
                    ),
                ),
                "classes": (
                    "collapse",
                    "less-dominant-style",
                    "nested-inline-flex-container",
                ),
            },
        ),
    )
    classes = ("less-dominant-style", "nested-inline-flex-container")

    inlines = [SuccessCriteriaReportInline]


class ObjectiveAndSuccessCriteriaInline(nested_admin.NestedTabularInline):
    model = ObjectiveAndSuccessCriteria
    extra = 1

    class Meta:
        pass

    list_display = ("objective", "details", "applicable_to_whole_operational_area")

    fields = ("objective", "details", "applicable_to_whole_operational_area")

    inlines = [SuccessCriteriaInline]


@admin.register(SuccessCriteriaLeftValue)
class SuccessCriteriaLeftValueAdmin(admin.ModelAdmin):
    model = SuccessCriteriaLeftValue

    list_display = (
        "name",
        "display_name",
    )


@admin.register(SuccessCriteriaComparisonOperator)
class SuccessCriteriaComparisonOperatorAdmin(admin.ModelAdmin):
    model = SuccessCriteriaComparisonOperator

    list_display = (
        "name",
        "display_name",
    )


@admin.register(SuccessCriteria)
class SuccessCriteriaAdmin(admin.ModelAdmin):
    model = SuccessCriteria

    list_display = (
        "name",
        "display_name",
        "left_value",
        "comparison_operator",
        "right_value_or_free_text",
    )


@admin.register(Objective)
class ObjectiveAdmin(admin.ModelAdmin):
    model = Objective

    list_display = (
        "name",
        "display_name",
    )


@admin.register(ObjectiveAndSuccessCriteria)
class ObjectiveAndSuccessCriteriaAdmin(nested_admin.NestedModelAdmin):
    model = ObjectiveAndSuccessCriteria

    list_display = (
        "objective",
        "details",
        "applicable_to_whole_operational_area",
    )

    inlines = [SuccessCriteriaInline]


class OperationalPlanRiskCategoryInline(nested_admin.NestedStackedInline):
    model = OperationalPlanRiskCategory
    extra = 0
    verbose_name = "Risk category"
    verbose_name_plural = "Risk categories"

    class Media:
        css = {
            "all": ["admin/class_media/css/inline_fieldsets.css"],
        }

    fieldsets = (
        (
            "Risk category",
            {
                "fields": (("risk_category",),),
                "classes": (
                    "collapse",
                    "less-dominant-style",
                    "nested-inline-flex-container",
                ),
            },
        ),
    )

    inlines = [OperationalPlanRiskCategoryContributingFactorInline]


class SelectWithOptionAttribute(forms.Select):
    def create_option(
        self, name, value, label, selected, index, subindex=None, attrs=None
    ):
        # This allows using strings labels as usual
        if isinstance(label, dict):
            opt_attrs = label.copy()
            label = opt_attrs.pop("label")
        else:
            opt_attrs = {}
        option_dict = super().create_option(
            name, value, label, selected, index, subindex=subindex, attrs=attrs
        )
        for key, val in opt_attrs.items():
            option_dict["attrs"][key] = val
        return option_dict


class ModelLegalApprovalChoiceField(forms.ModelChoiceField):
    widget = SelectWithOptionAttribute

    def label_from_instance(self, obj):
        return {
            "label": super().label_from_instance(obj),
            "data-has-additional-permissions": str(obj.has_additional_permissions),
            "data-is-shire-approval": str(obj.is_shire_approval),
        }


class ModelLegalApprovalInlineForm(forms.ModelForm):
    legal_approval = ModelLegalApprovalChoiceField(queryset=LegalApproval.objects.all())

    class Meta:
        model = ModelLegalApproval
        fields = "__all__"

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def clean(self):
        cleaned_data = super().clean()

        return cleaned_data


class ModelLegalApprovalInlineFormSet(BaseGenericInlineFormSet):
    def clean(self):
        has_approval = {"shire": False, "owner": False, "other": False}
        for form in self.forms:
            if self.can_delete and self._should_delete_form(form):
                continue
            legal_approval = form.cleaned_data.get("legal_approval", None)
            has_approval[legal_approval.land_type] = True

        # if self.instance.requires_shire_approvals and not has_approval["shire"]:
        #     raise forms.ValidationError(
        #         "This operational plan requires a shire approval but none have been added."
        #     )
        # if self.instance.requires_owner_approvals and not has_approval["owner"]:
        #     raise forms.ValidationError(
        #         "This operational plan requires an owner approval but none have been added."
        #     )
        # if self.instance.requires_other_land_approval and not has_approval["other"]:
        #     raise forms.ValidationError(
        #         "This operational plan requires an other land approval but none have been added."
        #     )


class FileAsApprovalModelFileInline(nested_admin.NestedGenericStackedInline):
    model = ModelFile
    extra = 0
    verbose_name = "File as approval"

    class Media:
        css = {
            "all": ["admin/class_media/css/inline_fieldsets.css"],
        }

    classes = ("less-dominant-style", "nested-inline-flex-container")


class ModelLegalApprovalInline(nested_admin.NestedGenericStackedInline):
    model = ModelLegalApproval
    extra = 0
    verbose_name = "Legal/Approval"
    verbose_name_plural = "Legal/Approvals"

    form = ModelLegalApprovalInlineForm
    formset = ModelLegalApprovalInlineFormSet

    class Media:
        js = (
            "admin/js/jquery.init.js",
            "admin/class_media/js/toggle_functions.js",
            "admin/class_media/js/operational_area_approval_admin.js",
        )
        css = {
            "all": ["admin/class_media/css/inline_fieldsets.css"],
        }

    class Meta:
        pass

    list_display = (
        "legal_approval",
        "has_additional_permissions",
        "text_as_approval",
        "text_remove_justification",
    )

    fieldsets = (
        (
            "Legal/Approval",
            {
                "fields": (("legal_approval",)),
                "classes": (
                    "legal-approval",
                    "less-dominant-style",
                ),
            },
        ),
        (
            "Land type",
            {
                "fields": (("lga",),),
                "classes": (
                    "additional-information-lga",
                    "less-dominant-style",
                    "hidden",
                ),
            },
        ),
        (
            "Documentation",
            {
                "fields": (
                    (
                        "text_as_approval",
                        "text_remove_justification",
                    )
                ),
                "classes": (
                    "additional-information-docs",
                    "less-dominant-style",
                    "hidden",
                ),
            },
        ),
    )

    inlines = [FileAsApprovalModelFileInline]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def get_formset(self, request, obj=None, **kwargs):
        form = super().get_formset(request, obj, **kwargs)

        return form


class ModelRequiredApprovalInline(nested_admin.NestedGenericTabularInline):
    model = ModelRequiredApproval
    extra = 0
    verbose_name = "Required Legal/Approval"
    verbose_name_plural = "Required Legal/Approvals"

    class Media:
        css = {
            "all": ["admin/class_media/css/inline_fieldsets.css"],
        }

    list_display = (
        "legal_approval_name",
        "is_required",
    )

    fields = (("display_name", "is_required"),)

    readonly_fields = ("display_name",)


class OperationalAreaAdminForm(forms.ModelForm):
    class Meta:
        model = OperationalArea
        fields = "__all__"
        help_texts = {
            "operational_area_different_from_bpu_rationale": "Rationale when operational area is different "
            "from burn planning unit.",
        }


@admin.register(OperationalArea)
class OperationalAreaAdmin(NestedDeleteRestrictedAdmin):
    model = OperationalArea

    form = OperationalAreaAdminForm

    class Media:
        js = (
            "admin/js/jquery.init.js",
            "admin/class_media/js/toggle_functions.js",
            "admin/class_media/js/operational_area_admin.js",
        )

    list_display = (
        "name",
        "burn_plan_element",
        "year",
        "operational_area_different_from_bpu_rationale",
        "district",
        "contentious_burn",
        "contentious_rationale",
    )

    fieldsets = (
        (
            "Details",
            {
                "fields": (
                    "name",
                    "burn_plan_element",
                    "year",
                    "operational_area_different_from_bpu_rationale",
                    "contentious_burn",
                ),
            },
        ),
        (
            "Contentious burn",
            {
                "fields": (("contentious_rationale",),),
                "classes": (
                    "admin-contentious-burn",
                    "less-dominant-style",
                ),
            },
        ),
        (
            "Spatial",
            {
                "fields": (
                    "district",
                    (
                        "polygon",
                        "linestring",
                    ),
                ),
            },
        ),
    )

    inlines = [
        ModelRequiredApprovalInline,
        ModelLegalApprovalInline,
    ]


class ContingencyNeighbourInline(nested_admin.NestedStackedInline):
    model = ContingencyNeighbour
    extra = 0
    verbose_name = "Neighbouring landowner or significant stakeholder"
    verbose_name_plural = "Neighbouring landowners and significant stakeholders"

    class Media:
        css = {
            "all": ["admin/class_media/css/inline_fieldsets.css"],
        }

    classes = ("less-dominant-style", "nested-inline-flex-container")


class ContingencyInline(nested_admin.NestedStackedInline):
    model = Contingency
    extra = 0

    class Media:
        css = {
            "all": ["admin/class_media/css/inline_fieldsets.css"],
        }

    fieldsets = (
        (
            "Contingency",
            {
                "fields": (("suppression_constraints",), "context_map"),
                "classes": (
                    "less-dominant-style",
                    "nested-inline-flex-container",
                ),
            },
        ),
    )

    readonly_fields = ("context_map",)

    inlines = [ContingencyNeighbourInline]


class ContextMapModelFileInline(nested_admin.NestedGenericStackedInline):
    model = ModelFile
    extra = 0
    verbose_name = "Context map"


class OperationalPlanAdminForm(forms.ModelForm):
    class Meta:
        model = OperationalPlan
        fields = "__all__"
        help_texts = {"window_of_opportunity": "Chance of completing burn if postponed"}


@admin.register(OperationalPlan)
class OperationalPlanAdmin(NestedDeleteRestrictedAdmin):
    model = OperationalPlan
    form = OperationalPlanAdminForm

    list_display = (
        "name",
        "operational_area",
        "operation_name",
        "operation",
        "operational_intent",
        "burn_priority",
        "window_of_opportunity",
        "context_description_of_burn",
        "context_risk_of_not_completing_burn",
        "context_operational_aspects",
        "prescription",
    )

    fieldsets = (
        (
            "Overview",
            {
                "fields": (
                    "name",
                    (
                        "reference_number",
                        "created",
                        "modified",
                    ),
                    "operational_area",
                    "operation_name",
                    "operation",
                    "operational_intent",
                ),
            },
        ),
        (
            "Priority",
            {
                "fields": (
                    "burn_priority",
                    "window_of_opportunity",
                ),
            },
        ),
        (
            "Context",
            {
                "fields": (
                    "context_description_of_burn",
                    "context_risk_of_not_completing_burn",
                    "context_operational_aspects",
                ),
            },
        ),
        (
            "Traffic",
            {
                "fields": ("traffic",),
            },
        ),
        (
            "Prescription",
            {
                "fields": ("prescription",),
            },
        ),
    )

    readonly_fields = ("reference_number", "created", "modified")

    inlines = [
        ContextMapModelFileInline,
        ObjectiveAndSuccessCriteriaInline,
        OperationalAreaPurposeInline,
        OperationalAreaProgramInline,
        OperationalPlanRiskCategoryInline,
        ContingencyInline,
        ModelLegalApprovalInline,
    ]


@admin.register(ContingencyNeighbour)
class ContingencyNeighbourAdmin(NestedDeleteRestrictedAdmin):
    model = ContingencyNeighbour

    list_display = (
        "contingency",
        "neighbour",
    )


@admin.register(Contingency)
class ContingencyAdmin(NestedDeleteRestrictedAdmin):
    model = Contingency

    list_display = (
        "name",
        "display_name",
        "suppression_constraints",
        "context_map",
    )

    fields = (
        "name",
        "display_name",
        "suppression_constraints",
        "context_map",
    )

    readonly_fields = ("context_map",)

    inlines = [ContingencyNeighbourInline]


class FireAssessmentSummaryModelFileInline(nested_admin.NestedGenericStackedInline):
    model = ModelFile
    extra = 0
    verbose_name = "Fire assessment summary"

    class Media:
        css = {
            "all": ["admin/class_media/css/inline_fieldsets.css"],
        }

    classes = ("less-dominant-style", "nested-inline-flex-container")


class FireBehaviourCalculationsModelFileInline(nested_admin.NestedGenericStackedInline):
    model = ModelFile
    extra = 0
    verbose_name = "Fire behaviour calculation"

    class Media:
        css = {
            "all": ["admin/class_media/css/inline_fieldsets.css"],
        }

    classes = ("less-dominant-style", "nested-inline-flex-container")


class PrescriptionFuelTypeInline(nested_admin.NestedStackedInline):
    model = PrescriptionFuelType
    extra = 0

    class Media:
        css = {
            "all": ["admin/class_media/css/inline_fieldsets.css"],
        }

    list_display = (
        "fuel_type",
        "cell_name",
        "scorch_height",
        "burn_area",
        "ros_range",
        "ffdi_range",
        "glc_range",
        "gfdi_range",
        "temperature_range",
        "rh_range",
        "sdi",
        "smc_range",
        "pmc_range",
        "wind_speed_range",
        "wind_direction",
    )

    fieldsets = (
        (
            "Fuel type",
            {
                "fields": (
                    (
                        "fuel_type",
                        "applicable_fuel_type_prescription_details",
                    ),
                ),
                "classes": (
                    "less-dominant-style",
                    "nested-inline-flex-container",
                ),
            },
        ),
        (
            "Fuel type prescription details",
            {
                "fields": (
                    (
                        "cell_name",
                        "scorch_height",
                        "burn_area",
                        "ros_range",
                        "ffdi_range",
                        "glc_range",
                        "gfdi_range",
                        "temperature_range",
                        "rh_range",
                        "sdi",
                        "smc_range",
                        "pmc_range",
                        "wind_speed_range",
                        "wind_direction",
                    ),
                ),
                "classes": (
                    "less-dominant-style",
                    "nested-inline-flex-container",
                ),
            },
        ),
    )

    readonly_fields = ("applicable_fuel_type_prescription_details",)

    inlines = [
        FireAssessmentSummaryModelFileInline,
        FireBehaviourCalculationsModelFileInline,
    ]

    def applicable_fuel_type_prescription_details(self, obj=None):
        """Return a list of applicable fuel type prescription details for the fuel type for purpose of display."""

        if not obj.applicable_fuel_type_prescription_details:
            return ""

        lis = format_html_join(
            "",
            "<li>&#x2022; {0}</li>",
            [(det.__str__(),) for det in obj.applicable_fuel_type_prescription_details],
        )
        return format_html("<ul style='margin-left:0px'>{}</ul>", lis)


@admin.register(Prescription)
class PrescriptionAdmin(NestedDeleteRestrictedAdmin):
    model = Prescription

    list_display = (
        "operational_overview",
        "ignition_sequence",
    )

    fields = (
        "operational_overview",
        "ignition_sequence",
    )

    inlines = [PrescriptionFuelTypeInline]
