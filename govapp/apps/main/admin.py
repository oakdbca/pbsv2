from django.contrib import admin

from .models import ModelFile


class ModelFileAdmin(admin.ModelAdmin):
    list_display = ("id", "file", "content_type", "object_id", "datetime_uploaded")


admin.site.register(ModelFile, ModelFileAdmin)
