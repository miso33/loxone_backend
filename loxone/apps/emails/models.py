from django.contrib.postgres.fields import ArrayField
from django.db import models

from loxone.core.models import BaseModel


class Email(BaseModel):
    recipients = ArrayField(models.CharField(max_length=200))
    recipients_copy = ArrayField(
        models.CharField(max_length=200), blank=True, null=True
    )
    recipients_blind_copy = ArrayField(
        models.CharField(max_length=200), blank=True, null=True
    )
    subject = models.CharField(max_length=1000, blank=True)
    body = models.CharField(max_length=1000, blank=True)
    body_link = models.CharField(max_length=1000, blank=True)
    data = models.JSONField(null=True)
    send_schedule = models.DateTimeField(auto_now_add=True)
    attempts_number = models.PositiveSmallIntegerField(default=0)
    sent_datetime = models.DateTimeField(null=True, blank=True)
    sent = models.BooleanField(default=False)

    class Meta:
        ordering = ["sent", "send_schedule"]
        default_related_name = "emails"

    def __str__(self):
        return str(self.recipients)
