from django.urls import path

from .views import individual_problem

urlpatterns = [
    path("problem/<int:pid>", individual_problem, name="problem_api"),
]
