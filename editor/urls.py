from django.urls import path

from .views import (
    EditorHomePageView,
    EditorCreateProblemView,
    EditorUpdateProblemView,
    EditorProblemDeleteView,
)

urlpatterns = [
    path("", EditorHomePageView.as_view(), name="editor_home"),
    path("create/", EditorCreateProblemView.as_view(), name="create_problem"),
    path("edit/<int:pk>/", EditorUpdateProblemView.as_view(), name="edit_problem"),
    path("delete/<int:pk>/", EditorProblemDeleteView.as_view(), name="delete_problem"),
]
