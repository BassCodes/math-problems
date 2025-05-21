from django.test import Client
from django.contrib.auth import get_user_model
from django.urls import reverse
from pytest_django.asserts import assertRedirects
import pytest


@pytest.mark.django_db
def test_problem_edit_permissions():
    client = Client()

    # Get request
    response = client.get(reverse("problem_edit", args=[1]))
    assertRedirects(
        response,
        reverse("login_page") + "?next=" + reverse("problem_edit", args=[1]),
    )
