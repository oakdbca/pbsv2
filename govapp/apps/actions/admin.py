from django.contrib import admin

from govapp.apps.main.admin import NestedDeleteRestrictedAdmin

from .models import Action


@admin.register(Action)
class ActionAdmin(NestedDeleteRestrictedAdmin):
    list_display = (
        "action",
        "responsibility",
        "category",
        "status",
        "date_created",
        "date_closed",
        "closed_by",
        "closed_details",
        "due_date_time",
    )

    fields = (
        "action",
        "responsibility",
        "category",
        "status",
        "date_created",
        "date_closed",
        "closed_by",
        "closed_details",
        "due_date_time",
    )

    readonly_fields = ("date_created",)
