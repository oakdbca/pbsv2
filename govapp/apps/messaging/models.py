import logging

from django.conf import settings
from django.contrib import auth
from django.db import models
from mailqueue.models import MailerMessage
from model_utils.models import TimeStampedModel

User = auth.get_user_model()

logger = logging.getLogger(__name__)


class MessageBatch(TimeStampedModel):
    """Used as a template to send messages to multiple groups and/or users."""

    groups: models.ManyToManyField = models.ManyToManyField(
        "auth.Group", related_name="%(class)smessage_batches", blank=True
    )
    users: models.ManyToManyField = models.ManyToManyField(
        User, related_name="%(class)smessage_batches", blank=True
    )
    sender = models.ForeignKey(
        User,
        related_name="%(class)s_sender",
        on_delete=models.PROTECT,
        null=True,
        blank=True,
    )  # If sender is null then it is a system message
    subject = models.CharField(max_length=100)
    content = models.TextField()
    html_content = models.TextField()
    dismissable = models.BooleanField(default=True)
    type = models.CharField(max_length=100, choices=settings.BOOTSTRAP_COLORS)
    send_email = models.BooleanField(default=False)
    sent = models.BooleanField(default=False)

    class Meta:
        verbose_name = "Message Batch"
        verbose_name_plural = "Message Batches"

    def __str__(self):
        return self.subject

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        if not self.sent:
            self.send()

    def send(self):
        users_to_send_to = User.objects.none()
        for group in self.groups.all():
            users_to_send_to = users_to_send_to.union(group.user_set.all())

        for user in users_to_send_to.filter():
            Message.objects.create(
                user=user,
                sender=self.sender,
                subject=self.subject,
                content=self.content,
                html_content=self.html_content,
                dismissable=self.dismissable,
                type=self.type,
                send_email=self.send_email,
            )

        self.sent = True
        self.save()

    def recall(self):
        self.messages.all().delete()


class MessageManager(models.Manager):
    def get_queryset(self) -> models.QuerySet:
        return super().get_queryset().select_related("user", "sender")


class Message(TimeStampedModel):
    message_batch = models.ForeignKey(
        MessageBatch,
        on_delete=models.PROTECT,
        related_name="messages",
        null=True,
        blank=True,
    )
    user = models.ForeignKey(
        User, related_name="%(class)s_messages", on_delete=models.PROTECT
    )
    sender = models.ForeignKey(
        User,
        related_name="%(class)s_sender",
        on_delete=models.PROTECT,
        null=True,
        blank=True,
    )  # If sender is null then it is a system message
    subject = models.CharField(max_length=100)
    content = models.TextField()
    html_content = models.TextField()
    dismissable = models.BooleanField(default=True)
    dismissed = models.BooleanField(default=False)
    type = models.CharField(max_length=100, choices=settings.BOOTSTRAP_COLORS)
    send_email = models.BooleanField(default=False)

    def __str__(self):
        return self.subject

    def save(self, *args, **kwargs):
        # Note: Overriden save method is atomic by default
        send_email = False

        # I thought it best to save the message first and then send the email
        # TODO: Decide if modifying a message should send another email? currently does not
        if not self.pk and self.send_email:
            send_email = True
        super().save(*args, **kwargs)
        if not send_email:
            return

        if not self.user.email:
            logger.warning(f"Message {self.id}: User {self.user} has no email address")

        message = MailerMessage()
        message.subject = self.subject
        message.to_address = self.user.email
        if self.sender:
            message.from_address = self.sender.email
        else:
            message.from_address = settings.DEFAULT_FROM_EMAIL
        message.content = self.content
        message.html_content = self.html_content
        message.app = Message._meta.app_label
        message.save()

    def has_object_permission(self, user: auth.models.User) -> bool:
        return user == self.user
