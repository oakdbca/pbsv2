from django.contrib import admin

from govapp.apps.main.admin import DeleteRestrictedAdmin

from .models import LegalApproval, OperationalArea, OperationalAreaRiskFactor


class OperationalAreaRiskFactorInline(admin.TabularInline):
    model = OperationalAreaRiskFactor
    extra = 0


class OperationalAreaApprovalInline(admin.TabularInline):
    model = OperationalArea.legal_approvals.through
    extra = 0
    verbose_name = "Operational Area Approval"
    verbose_name_plural = "Operational Area Approvals"


@admin.register(OperationalArea)
class OperationalAreaAdmin(DeleteRestrictedAdmin):
    model = OperationalArea
    list_display = (
        # "name",
        "operation_name",
    )

    inlines = [OperationalAreaApprovalInline, OperationalAreaRiskFactorInline]
    # exclude = ("output_leaders",)


@admin.register(LegalApproval)
class ApprovalAdmin(admin.ModelAdmin):
    model = LegalApproval
    list_display = ("approver",)


# admin.site.register(Approval, ApprovalAdmin)
