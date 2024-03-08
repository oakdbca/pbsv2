from django.contrib import admin

from .models import Message, MessageBatch


class MessageAdmin(admin.ModelAdmin):
    model = Message
    list_display = ("user", "sender", "subject", "created")


admin.site.register(MessageBatch)
admin.site.register(Message, MessageAdmin)
