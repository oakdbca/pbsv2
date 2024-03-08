from django.conf import settings
from django.contrib import auth
from django.db import models
from mailqueue.models import MailerMessage
from model_utils.models import TimeStampedModel

User = auth.get_user_model()


class MessageBatch(TimeStampedModel):
    """Used as a template to send messages to multiple groups and/or users."""

    groups: models.ManyToManyField = models.ManyToManyField(
        "auth.Group", related_name="%(class)smessage_batches"
    )
    users: models.ManyToManyField = models.ManyToManyField(
        User, related_name="%(class)smessage_batches"
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

    def send(self):
        if self.sent:
            raise ValueError("Message batch has already been sent")

        users_to_send_to = self.users.all()
        for group in self.groups.all():
            users_to_send_to = users_to_send_to.union(group.user_set.all())

        for user in users_to_send_to:
            Message.objects.create(
                to=user,
                sender=self.sender,
                subject=self.subject,
                body=self.body,
                dismissable=self.dismissable,
                type=self.type,
                send_email=self.send_email,
            )

        self.sent = True
        self.save()

    def recall(self):
        self.messages.all().delete()

    def __str__(self):
        return self.subject


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

        message = MailerMessage()
        message.subject = self.subject
        message.to_address = self.user.email
        if self.sender:
            message.from_address = f"{self.sender.full_name} <{self.sender.email}>"
        else:
            message.from_address = (
                f"{settings.PROJECT_NAME} <{settings.DEFAULT_FROM_EMAIL}"
            )

        message.content = self.content
        message.html_content = self.html_content
        message.app = Message._meta.app_label
        message.save()
