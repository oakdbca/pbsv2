from django import forms
from django.contrib import admin
from model_utils import Choices

from .models import AuthorityToTake, LegalApproval


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


@admin.register(AuthorityToTake)
class AuthorityToTakeAdmin(admin.ModelAdmin):
    model = AuthorityToTake

    list_display = (
        "application",
        "issuance",
    )


@admin.register(LegalApproval)
class LegalApprovalAdmin(admin.ModelAdmin):
    model = LegalApproval
    form = LegalApprovalAdminForm

    list_display = (
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
