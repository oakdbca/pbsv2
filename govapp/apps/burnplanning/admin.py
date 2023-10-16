from django.contrib import admin

from govapp.apps.main.admin import DeleteRestrictedAdmin

from .models import BurnPlanUnit, BurnPlanUnitDistrict


class BurnPlanUnitDistrictInline(admin.TabularInline):
    model = BurnPlanUnitDistrict
    extra = 0


class BurnPlanUnitAdmin(admin.ModelAdmin):
    inlines = [BurnPlanUnitDistrictInline]


class BurnPlanUnitDistrictAdmin(DeleteRestrictedAdmin):
    pass


admin.site.register(BurnPlanUnit, BurnPlanUnitAdmin)
