import nested_admin
from django import forms
from django.contrib import admin

from govapp.apps.main.admin import DeleteRestrictedAdmin, NestedDeleteRestrictedAdmin

from .models import (
    Consequence,
    ContributingFactor,
    ContributingFactorStandardControl,
    Likelihood,
    LikelihoodOfConsequence,
    OverwriteControl,
    RiskCategory,
    RiskLevel,
    RiskRating,
    StandardControl,
)


@admin.register(StandardControl)
class StandardControlAdmin(DeleteRestrictedAdmin):
    model = StandardControl
    list_display = ("name",)


@admin.register(OverwriteControl)
class OverwriteControlAdmin(DeleteRestrictedAdmin):
    model = OverwriteControl
    list_display = ("name", "standard_control")


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


@admin.register(Consequence)
class ConsequenceAdmin(DeleteRestrictedAdmin):
    model = Consequence
    list_display = ("name",)


@admin.register(Likelihood)
class LikelihoodAdmin(DeleteRestrictedAdmin):
    model = Likelihood
    list_display = ("name", "ordinal_scale")


@admin.register(RiskLevel)
class RiskLevelAdmin(DeleteRestrictedAdmin):
    model = RiskLevel
    list_display = ("name", "ordinal_scale", "requires_additional_controls")


@admin.register(LikelihoodOfConsequence)
class LikelihoodOfConsequenceAdmin(DeleteRestrictedAdmin):
    model = LikelihoodOfConsequence
    list_display = ("consequence", "likelihood", "risk_level")


@admin.register(RiskRating)
class RiskRatingAdmin(DeleteRestrictedAdmin):
    model = RiskRating
    list_display = ("consequence", "likelihood", "risk_level")

    fields = ("consequence", "likelihood", "risk_level")
    readonly_fields = ("risk_level",)
