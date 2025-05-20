from django.db import models
import uuid
from django.urls import reverse

from django.contrib.auth.models import AbstractUser

from problems.models import Problem


class CustomUser(AbstractUser):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)

    description = models.TextField(blank=True, null=True)

    def get_absolute_url(self):
        return reverse("user_profile", kwargs={"pk": self.pk})

    def __str__(self):
        return self.username


class UserSolvedProblem(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    problem = models.ForeignKey(Problem, on_delete=models.CASCADE)
    solve_date = models.DateTimeField()
