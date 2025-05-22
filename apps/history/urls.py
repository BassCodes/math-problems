from django.urls import path

from .views import ProblemHistoryView

urlpatterns = [
    path("problems/<int:pk>", ProblemHistoryView.as_view(), name="problem_history"),
]
