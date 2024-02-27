from django import forms
from django.contrib import admin
from model_utils import Choices

from .models import (
    AuthorityToTake,
    DisturbanceApplication,
    LegalApproval,
    OtherApproval,
)


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
            "provide free text as approval, or remove the additional required approval if a "
            "justification is provided.",
        }


@admin.register(OtherApproval)
class OtherApprovalAdmin(admin.ModelAdmin):
    model = OtherApproval

    list_display = (
        "reference_number",
        "lodgement_date",
        "issue_date",
        "approval_date",
        "expiry_date",
    )

    fields = (
        "reference_number",
        "lodgement_date",
        "issue_date",
        "approval_date",
        "expiry_date",
    )


@admin.register(DisturbanceApplication)
class DisturbanceApplicationAdmin(admin.ModelAdmin):
    model = DisturbanceApplication

    list_display = (
        "proposal",
        "approval",
    )


@admin.register(AuthorityToTake)
class AuthorityToTakeAdmin(admin.ModelAdmin):
    model = AuthorityToTake

    list_display = (
        "application",
        "issuance",
    )

    class Meta:
        verbose_name = "Authority to take"
        verbose_name_plural = "Authorities to take"


@admin.register(LegalApproval)
class LegalApprovalAdmin(admin.ModelAdmin):
    model = LegalApproval
    form = LegalApprovalAdminForm

    list_display = (
        "name",
        "approver",
        "approval_type",
        "land_type",
        "has_additional_permissions",
        "is_required_for_operational_area",
        "is_required_for_operational_plan",
    )

    fieldsets = (
        (
            None,
            {
                "fields": ("name",),
            },
        ),
        (
            "General information",
            {
                "fields": (
                    (
                        "approver",
                        "approval_type",
                        "land_type",
                        "has_additional_permissions",
                        (
                            "is_required_for_operational_area",
                            "is_required_for_operational_plan",
                        ),
                    )
                ),
            },
        ),
    )
