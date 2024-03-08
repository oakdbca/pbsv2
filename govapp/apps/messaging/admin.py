from django.contrib import admin

from .models import Message, MessageBatch


class MessageBatchAdmin(admin.ModelAdmin):
    model = MessageBatch
    list_display = ("sender", "subject", "created")
    filter_horizontal = (
        "groups",
        "users",
    )


class MessageAdmin(admin.ModelAdmin):
    model = Message
    list_display = ("user", "sender", "subject", "created")


admin.site.register(MessageBatch, MessageBatchAdmin)
admin.site.register(Message, MessageAdmin)
