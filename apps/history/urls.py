from django.urls import path

from .views import ProblemHistoryView, SourceHistoryView

urlpatterns = [
    path("problem/<int:pk>", ProblemHistoryView.as_view(), name="problem_history"),
    path("source/<slug:slug>", SourceHistoryView.as_view(), name="source_history"),
]
