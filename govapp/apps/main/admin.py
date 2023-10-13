from django.contrib import admin

from .models import District, ModelFile, Region


class ModelFileAdmin(admin.ModelAdmin):
    list_display = ("id", "file", "content_type", "object_id", "datetime_uploaded")


class RegionAdmin(admin.ModelAdmin):
    list_display = ("id", "name", "display_name")


class DistrictAdmin(admin.ModelAdmin):
    list_display = ("id", "name", "display_name")


admin.site.register(ModelFile, ModelFileAdmin)
admin.site.register(Region, RegionAdmin)
admin.site.register(District, DistrictAdmin)
