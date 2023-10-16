from django.contrib import admin

from govapp.apps.main.admin import DeleteRestrictedAdmin

from .models import BurnPlanUnit, BurnPlanUnitDistrict


class BurnPlanUnitAdmin(admin.ModelAdmin):
    pass


class BurnPlanUnitDistrictAdmin(DeleteRestrictedAdmin):
    pass


admin.site.register(BurnPlanUnit, BurnPlanUnitAdmin)
admin.site.register(BurnPlanUnitDistrict, BurnPlanUnitDistrictAdmin)
