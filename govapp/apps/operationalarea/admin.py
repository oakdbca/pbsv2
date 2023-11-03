from django import forms
from django.contrib import admin

from govapp.apps.main.admin import DeleteRestrictedAdmin

from .models import (
    LegalApproval,
    OperationalArea,
    OperationalAreaApproval,
    OperationalAreaRiskFactor,
)


class LegalApprovalAdminForm(forms.ModelForm):
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

    class Media:
        js = (
            "admin/js/jquery.init.js",
            "admin/class_media/js/legal_approval_admin.js",
        )

    list_display = (
        "approver",
        "approval_type",
        "lga",
        "has_additional_permissions",
        "text_as_approval",
        "text_remove_justification",
    )

    fieldsets = (
        (
            "General information",
            {
                "fields": (
                    (
                        "approver",
                        "approval_type",
                        "lga",
                        "has_additional_permissions",
                    )
                ),
            },
        ),
        (
            "Additional information",
            {
                "fields": (
                    (
                        "file_as_approval",
                        "text_as_approval",
                        "text_remove_justification",
                    )
                ),
                "classes": ("additional-information",),
            },
        ),
    )


class OperationalAreaRiskFactorInline(admin.TabularInline):
    model = OperationalAreaRiskFactor
    extra = 0


class OperationalAreaApprovalInline(admin.TabularInline):
    model = OperationalAreaApproval
    extra = 1
    verbose_name = "Operational Area Approval"
    verbose_name_plural = "Operational Area Approvals"

    class Meta:
        pass


@admin.register(OperationalArea)
class OperationalAreaAdmin(DeleteRestrictedAdmin):
    model = OperationalArea
    list_display = (
        # "name",
        "operation_name",
    )

    inlines = [OperationalAreaApprovalInline, OperationalAreaRiskFactorInline]
