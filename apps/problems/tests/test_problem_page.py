from django.urls import reverse

import pytest

from problems.models import Problem, Source


@pytest.mark.django_db
def test_problem_viewing(client):
    source = Source.objects.create(name="test source", slug="test")
    response = client.get(
        reverse("problem_detail", kwargs={"slug": "test", "number": 7})
    )
    assert response.status_code == 404
    problem = Problem.objects.create(
        problem_text="problem text",
        source=source,
        number=7,
    )
    response = client.get(
        reverse("problem_detail", kwargs={"slug": "test", "number": problem.number})
    )
    print(response.content.decode())
    assert response.status_code == 200
