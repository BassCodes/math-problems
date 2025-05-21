from django.urls import path


from .views import (
    EditorHomePageView,
    EditorProblemDeleteView,
    IncompleteSourceView,
    problem_create_view,
    problem_update_view,
    SolutionDeleteView,
    SourceEditView,
    SourceCreateView,
    SourceGroupEditView,
    SourceGroupCreateView,
)

urlpatterns = [
    path("", EditorHomePageView.as_view(), name="editor_home"),
    path("missing/", IncompleteSourceView.as_view(), name="missing_problems"),
    path(
        "solution/del/<int:pk>",
        SolutionDeleteView.as_view(),
        name="solution_delete",
    ),
    path("problem/add/", problem_create_view, name="problem_create"),
    path("problem/upd/<int:pk>/", problem_update_view, name="problem_edit"),
    path(
        "problem/del/<int:pk>/",
        EditorProblemDeleteView.as_view(),
        name="problem_delete",
    ),
    path("source/upd/<int:pk>", SourceEditView.as_view(), name="source_edit"),
    path("source/add/", SourceCreateView.as_view(), name="source_create"),
    path(
        "sourcegroup/upd/<int:pk>",
        SourceGroupEditView.as_view(),
        name="sourcegroup_edit",
    ),
    path(
        "sourcegroup/add/", SourceGroupCreateView.as_view(), name="sourcegroup_create"
    ),
]
