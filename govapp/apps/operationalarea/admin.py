from django.contrib import admin

from govapp.apps.main.admin import DeleteRestrictedAdmin

from .models import OperationalArea, OperationalAreaApproval


@admin.register(OperationalArea)
class OperationalAreaAdmin(DeleteRestrictedAdmin):
    model = OperationalArea
    list_display = (
        # "name",
        "operation_name",
    )
    # exclude = ("output_leaders",)


@admin.register(OperationalAreaApproval)
class ApprovalAdmin(admin.ModelAdmin):
    model = OperationalAreaApproval
    list_display = ("approver",)


# admin.site.register(Approval, ApprovalAdmin)
