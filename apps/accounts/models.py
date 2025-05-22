from django.db import models
import uuid
from django.urls import reverse

from django.contrib.auth.models import AbstractUser
from django.utils.translation import gettext as _

from .validators import CustomAsciiUsernameValidator


class CustomUser(AbstractUser):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)

    username_validator = CustomAsciiUsernameValidator()

    username = models.CharField(
        _("username"),
        max_length=18,
        unique=True,
        help_text=_(
            "Required. 30 characters or fewer. Lowercase letters, digits and underscores(_) only."
        ),
        validators=[username_validator],
        error_messages={
            "unique": _("A user with that username already exists."),
        },
    )
    description = models.TextField(blank=True, null=True)

    def get_absolute_url(self):
        return reverse("user_profile", kwargs={"pk": self.pk})

    def __str__(self):
        return self.username
