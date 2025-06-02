from django.db import models

from accounts.models import CustomUser


class HistoryPublishDataShim(models.Model):
    class Meta:
        abstract = True

    class PublishType(models.TextChoices):
        FORCE_PUBLISHED = ("FR", "Force Published")
        MERGED = ("MR", "Merged by review")

    history_publish_type = models.CharField(max_length=2, choices=PublishType, null=True)
    history_publish_reviewer = models.ForeignKey(CustomUser, on_delete=models.SET_NULL, null=True, related_name="+")
    history_publish_author = models.ForeignKey(CustomUser, on_delete=models.SET_NULL, null=True, related_name="+")
