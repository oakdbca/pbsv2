# Third-Party
from django.contrib import auth
from django.contrib.contenttypes import fields
from django.contrib.contenttypes import models as ct_models
from django.db import models
from django.utils.text import slugify
from protected_media.models import ProtectedFileField

# Shortcuts
UserModel = auth.get_user_model()


class CommunicationsLogEntryType(models.IntegerChoices):
    """Enumeration for a Communications Log Entry Type."""

    EMAIL = 1
    PHONE = 2
    MAIL = 3
    PERSON = 4
    OTHER = 5


class CommunicationsLogEntry(models.Model):
    """Model for a Communications Log Entry."""

    objects: models.Manager

    content_type = models.ForeignKey(ct_models.ContentType, on_delete=models.CASCADE)
    object_id = models.PositiveIntegerField()
    content_object = fields.GenericForeignKey("content_type", "object_id")

    # Communications Log Entry Fields
    created_at = models.DateTimeField(auto_now_add=True)
    type = models.IntegerField(choices=CommunicationsLogEntryType.choices)  # noqa: A003
    to = models.TextField(blank=True)
    cc = models.TextField(blank=True)
    fromm = models.TextField(blank=True)
    subject = models.TextField(blank=True)
    text = models.TextField(blank=True)
    user = models.ForeignKey(
        UserModel, related_name="communications_log_entries", on_delete=models.CASCADE
    )

    class Meta:
        verbose_name = "Communications Log Entry"
        verbose_name_plural = "Communications Log Entries"

    def __str__(self) -> str:
        return f"{self.content_type.name} - {self.content_object}"

    @property
    def username(self) -> str:
        return self.user.username


def communications_log_document_upload_location(instance, filename):
    content_type_name = slugify(instance.entry.content_type.name)
    object_id = instance.entry.object_id
    return f"uploads/{content_type_name}/{object_id}/communications-log-documents/{filename}"


class CommunicationsLogDocument(models.Model):
    """Model for a Communications Log Document."""

    name = models.TextField(blank=True)
    description = models.TextField(blank=True)
    uploaded_at = models.DateTimeField(auto_now_add=True)
    entry = models.ForeignKey(
        CommunicationsLogEntry, related_name="documents", on_delete=models.CASCADE
    )
    file = ProtectedFileField(upload_to=communications_log_document_upload_location)

    class Meta:
        verbose_name = "Communications Log Document"
        verbose_name_plural = "Communications Log Documents"

    def __str__(self) -> str:
        # Generate String and Return
        return f"{self.file}"


class ActionsLogEntry(models.Model):
    objects: models.Manager

    content_type = models.ForeignKey(ct_models.ContentType, on_delete=models.CASCADE)
    object_id = models.PositiveIntegerField()
    content_object = fields.GenericForeignKey("content_type", "object_id")

    # Actions Log Entry Fields
    who = models.ForeignKey(
        UserModel, related_name="actions_log_entries", on_delete=models.CASCADE
    )
    when = models.DateTimeField(auto_now_add=True)
    what = models.TextField()

    class Meta:
        """Actions Log Entry Model Metadata."""

        verbose_name = "Actions Log Entry"
        verbose_name_plural = "Actions Log Entries"

    def __str__(self) -> str:
        return f"{self.content_type.name} - {self.content_object}"

    @property
    def username(self) -> str:
        return self.who.username
