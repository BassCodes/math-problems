from django.test import TestCase, Client
from django.contrib.auth import get_user_model
from django.urls import reverse
from urllib.parse import urlencode

from problems.models import Problem, Source


class ProblemTests(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.user = get_user_model().objects.create_user(
            username="username", password="password"
        )
        cls.source = Source.objects.create(name="test")

        cls.problem = Problem.objects.create(
            problem_text="a",
            number=1,
        )

    def test_problem_edit_permissions(self):
        # Attempt to try editing a problem without permissions
        self.client.login(username="username", password="password")

        # Get request
        response = self.client.get(reverse("problem_edit", args=[1]))
        self.assertRedirects(
            response,
            reverse("login_page") + "?next=" + reverse("problem_edit", args=[1]),
        )

        # Post request
        response = self.client.post(
            reverse("problem_edit", args=[1]),
        )
        self.assertRedirects(
            response,
            reverse("login_page") + "?next=" + reverse("problem_edit", args=[1]),
        )
