from django.db import models
import uuid
from django.urls import reverse

from django.contrib.auth.models import AbstractUser


class CustomUser(AbstractUser):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)

    description = models.TextField(blank=True, null=True)

    def get_absolute_url(self):
        return reverse("user_profile", kwargs={"pk": self.pk})

    def __str__(self):
        return self.username
