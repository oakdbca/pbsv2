import nested_admin
from django import forms
from django.contrib import admin

from govapp.apps.main.admin import DeleteRestrictedAdmin, NestedDeleteRestrictedAdmin

from .models import (
    ContributingFactor,
    ContributingFactorStandardControl,
    RiskCategory,
    StandardControl,
)


@admin.register(StandardControl)
class StandardControlAdmin(DeleteRestrictedAdmin):
    model = StandardControl
    list_display = ("name",)


class ContributingFactorStandardControlInline(nested_admin.NestedTabularInline):
    model = ContributingFactorStandardControl
    extra = 0


class ContributingFactorForm(forms.ModelForm):
    class Meta:
        model = ContributingFactor
        fields = "__all__"
        help_texts = {
            "factors": "The interval this contributing factor covers, "
            "including the lower and excluding the upper bound. "
            "Empty values means no bound.",
        }


@admin.register(ContributingFactor)
class ContributingFactorAdmin(NestedDeleteRestrictedAdmin):
    model = ContributingFactor
    form = ContributingFactorForm

    list_display = (
        "name",
        "factors",
    )

    inlines = [
        ContributingFactorStandardControlInline,
    ]


@admin.register(RiskCategory)
class RiskCategoryAdmin(DeleteRestrictedAdmin):
    model = RiskCategory
    list_display = ("name",)
