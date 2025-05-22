from django.urls import path

from .views import ProblemHistoryView

urlpatterns = [
    path("problem/<int:pk>", ProblemHistoryView.as_view(), name="problem_history"),
]
