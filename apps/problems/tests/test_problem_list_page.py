from django.urls import reverse

from pytest_django.asserts import assertInHTML
import pytest


@pytest.mark.django_db
def test_problem_list_without_problems(client):
    response = client.get(reverse("problem_list"))
    assert response.status_code == 200

    assertInHTML("(No results found)", response.content.decode())
