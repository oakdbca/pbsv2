from django.contrib import admin
from django.db import models

from govapp.apps.main.admin import NestedDeleteRestrictedAdmin
from govapp.apps.main.models import RichTextEditorWidget

from .models import Action, ActionResponsibility


@admin.register(Action)
class ActionAdmin(NestedDeleteRestrictedAdmin):
    list_display = (
        "content_object",
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
        (
            "action",
            "category",
        ),
        (
            "responsibility",
            "status",
        ),
        "date_created",
        (
            "date_closed",
            "closed_by",
            "closed_details",
        ),
        "due_date_time",
        (
            "content_type",
            "object_id",
        ),
    )

    readonly_fields = (
        "date_created",
        "content_type",
        "object_id",
    )

    formfield_overrides = {
        models.TextField: {"widget": RichTextEditorWidget(rows=2, cols=30)},
    }

    def has_add_permission(self, request, obj=None):
        # Disable the add button, as we want to create Actions via the models that implement them as a GenericRelation
        return False


@admin.register(ActionResponsibility)
class ActionResponsibilityAdmin(NestedDeleteRestrictedAdmin):
    pass
