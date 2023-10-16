from django.contrib import admin

from govapp.apps.main.admin import DeleteRestrictedAdmin

from .models import (
    BurnPlanElement,
    BurnPlanUnit,
    BurnPlanUnitDistrict,
    Justification,
    OutputLeaderType,
    Program,
    Purpose,
    Treatment,
)


class BurnPlanUnitDistrictInline(admin.TabularInline):
    model = BurnPlanUnitDistrict
    extra = 0


class BurnPlanUnitAdmin(admin.ModelAdmin):
    inlines = [BurnPlanUnitDistrictInline]


class OutputLeaderInline(admin.TabularInline):
    model = BurnPlanElement.output_leaders.through
    verbose_name = "Output Leader"
    verbose_name_plural = "Output Leaders"
    extra = 0


class BurnPlanElementAdmin(DeleteRestrictedAdmin):
    inlines = [OutputLeaderInline]
    exclude = ("output_leaders",)


admin.site.register(BurnPlanUnit, BurnPlanUnitAdmin)
admin.site.register(BurnPlanElement, BurnPlanElementAdmin)

admin.site.register(Treatment)
admin.site.register(Justification)
admin.site.register(Purpose)
admin.site.register(Program)
admin.site.register(OutputLeaderType)
