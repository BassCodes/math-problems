from django.urls import path

from .views import (
    EditorHomePageView,
    EditorProblemDeleteView,
    EditorMissingProblemsView,
    EditorIncompleteSourceView,
    problem_create_view,
    problem_update_view

)

urlpatterns = [
    path("", EditorHomePageView.as_view(), name="editor_home"),
    path("create/", problem_create_view, name="create_problem"),
    path("missing/", EditorMissingProblemsView.as_view(), name="missing_problems"),
    path("missing/<int:pk>", EditorIncompleteSourceView.as_view(), name="missing_problem"),
    path("edit/<int:pk>/", problem_update_view, name="edit_problem"),
    path("delete/<int:pk>/", EditorProblemDeleteView.as_view(), name="delete_problem"),
]
