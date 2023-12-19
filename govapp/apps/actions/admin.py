import nested_admin
from django.contrib import admin
from django.db import models

from govapp.apps.main.admin import NestedDeleteRestrictedAdmin
from govapp.apps.main.models import ModelFile, RichTextEditorWidget

from .models import Action, ActionResponsibility


class ActionDocumentsModelFileInline(nested_admin.NestedGenericStackedInline):
    model = ModelFile
    extra = 0
    verbose_name = "Document"
    verbose_name_plural = "Documents"

    class Media:
        css = {
            "all": ["admin/class_media/css/inline_fieldsets.css"],
        }

    classes = ("less-dominant-style", "nested-inline-flex-container")


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

    inlines = [
        ActionDocumentsModelFileInline,
    ]

    formfield_overrides = {
        models.TextField: {"widget": RichTextEditorWidget(rows=2, cols=30)},
    }

    def has_add_permission(self, request, obj=None):
        # Disable the add button, as we want to create Actions via the models that implement them as a GenericRelation
        return False


@admin.register(ActionResponsibility)
class ActionResponsibilityAdmin(NestedDeleteRestrictedAdmin):
    pass
