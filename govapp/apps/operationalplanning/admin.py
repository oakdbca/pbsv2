from logging import getLogger

import nested_admin
from django import forms
from django.contrib import admin
from model_utils import Choices

from govapp.apps.main.admin import DeleteRestrictedAdmin, NestedDeleteRestrictedAdmin
from govapp.apps.risk.models import ContributingFactorStandardControl

from .models import (
    LegalApproval,
    Objective,
    ObjectiveAndSuccessCriteria,
    OperationalArea,
    OperationalPlan,
    OperationalPlanApproval,
    OperationalPlanProgram,
    OperationalPlanPurpose,
    OperationalPlanRiskCategory,
    OperationalPlanRiskCategoryContributingFactor,
    OperationalPlanRiskCategoryContributingFactorAdditionalControl,
    OperationalPlanRiskCategoryContributingFactorAdditionalControlRiskRating,
    OperationalPlanRiskCategoryContributingFactorOverwriteControl,
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


class LegalApprovalAdminForm(forms.ModelForm):
    approval_type = forms.ChoiceField(
        choices=LegalApproval.APPROVAL_TYPES, required=True
    )  # This hides the null/empty option
    land_type = forms.ChoiceField(
        choices=Choices(("", "N/A")) + LegalApproval.LAND_TYPES, required=False
    )  # This adds a null/empty option

    class Meta:
        model = LegalApproval
        fields = "__all__"
        help_texts = {
            "has_additional_permissions": "Check to allow the user to attach a file as approval, "
            "provide free text as approval, or remove the required approval."
        }


@admin.register(LegalApproval)
class LegalApprovalAdmin(admin.ModelAdmin):
    model = LegalApproval
    form = LegalApprovalAdminForm

    list_display = (
        "approver",
        "approval_type",
        "land_type",
        "has_additional_permissions",
    )

    fieldsets = (
        (
            "General information",
            {
                "fields": (
                    (
                        "approver",
                        "approval_type",
                        "land_type",
                        "has_additional_permissions",
                    )
                ),
            },
        ),
    )


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


class OperationalAreaApprovalChoiceField(forms.ModelChoiceField):
    widget = SelectWithOptionAttribute

    def label_from_instance(self, obj):
        return {
            "label": super().label_from_instance(obj),
            "data-has-additional-permissions": str(obj.has_additional_permissions),
            "data-is-shire-approval": str(obj.is_shire_approval),
        }


class OperationalAreaApprovalAdminForm(forms.ModelForm):
    legal_approval = OperationalAreaApprovalChoiceField(
        queryset=LegalApproval.objects.all()
    )

    class Meta:
        model = OperationalPlanApproval
        fields = "__all__"

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def clean(self):
        cleaned_data = super().clean()

        return cleaned_data


class OperationalPlanApprovalInline(nested_admin.NestedStackedInline):
    model = OperationalPlanApproval
    extra = 0
    verbose_name = "Operational Area Approval"
    verbose_name_plural = "Operational Area Approvals"

    form = OperationalAreaApprovalAdminForm

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
        "file_as_approval",
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
                        "file_as_approval",
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

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def get_formset(self, request, obj=None, **kwargs):
        form = super().get_formset(request, obj, **kwargs)

        return form


class OperationalAreaAdminForm(forms.ModelForm):
    class Meta:
        model = OperationalArea
        fields = "__all__"
        help_texts = {
            "operational_area_different_from_bpu_rationale": "Rationale when operational area is different "
            "from burn planning unit."
        }


@admin.register(OperationalArea)
class OperationalAreaAdmin(DeleteRestrictedAdmin):
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
        "context_map",
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
                    "context_map",
                ),
            },
        ),
        (
            "Traffic",
            {
                "fields": ("traffic",),
            },
        ),
    )

    readonly_fields = ("reference_number", "created", "modified")

    inlines = [
        ObjectiveAndSuccessCriteriaInline,
        OperationalAreaPurposeInline,
        OperationalAreaProgramInline,
        OperationalPlanRiskCategoryInline,
        OperationalPlanApprovalInline,
    ]
