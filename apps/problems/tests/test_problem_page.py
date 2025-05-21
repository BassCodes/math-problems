from django.urls import reverse

import pytest

from problems.models import Problem, Source


@pytest.mark.django_db
def test_problem_viewing(client):
    response = client.get(reverse("problem_detail", kwargs={"pk": 1}))
    assert response.status_code == 404
    source = Source.objects.create(name="test source")
    problem = Problem.objects.create(
        problem_text="problem text",
        source=source,
        number=7,
    )
    response = client.get(reverse("problem_detail", kwargs={"pk": problem.id}))
    print(response.content.decode())
    assert response.status_code == 200
