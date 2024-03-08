from django.contrib import admin

from .models import Message, MessageBatch

admin.site.register(MessageBatch)
admin.site.register(Message)
