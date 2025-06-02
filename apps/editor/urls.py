from django.urls import path


from .views import (
    # Misc Views
    IncompleteSourceView,
    UserDraftsDetailView,
    MyDraftsDetailView,
    # Draft Preview Views
    DraftSourceView,
    DraftSourceGroupView,
    DraftProblemView,
    # Draft Create Views
    DraftSourceCreateView,
    DraftSourceGroupCreateView,
    DraftProblemCreateView,
    DraftSolutionCreateView,
    # Draft Edit Views
    DraftSourceEditView,
    DraftSourceGroupEditView,
    DraftProblemEditView,
    # Draft Delete Views
    DraftSourceDelete,
    DraftSourceGroupDelete,
    DraftProblemDelete,
    DraftSolutionDelete,
    # Draft Force-publish Views
    DraftSourceForcePublishView,
    DraftSourceGroupForcePublishView,
    DraftProblemForcePublishView,
    DraftSolutionForcePublishView,
    # Object Forked Views
    SourceForkView,
    SourceGroupForkView,
    ProblemForkView,
    SolutionForkView,
)

urlpatterns = [
    path("missing", IncompleteSourceView.as_view(), name="missing_problems"),
    path("drafts/<uuid:pk>", UserDraftsDetailView.as_view(), name="user_drafts"),
    path("drafts/", MyDraftsDetailView.as_view(), name="my_drafts"),
    # Draft Preview Views
    path("drafts/source/<int:pk>", DraftSourceView.as_view(), name="draft_source"),
    path("drafts/source_group/<int:pk>", DraftSourceGroupView.as_view(), name="draft_source_group"),
    path("drafts/problem/<int:pk>", DraftProblemView.as_view(), name="draft_problem"),
    # Draft Create Views
    path("drafts/source/new", DraftSourceCreateView.as_view(), name="draft_source_new"),
    path("drafts/source_group/new", DraftSourceGroupCreateView.as_view(), name="draft_source_group_new"),
    path("drafts/problem/new", DraftProblemCreateView.as_view(), name="draft_problem_new"),
    path("drafts/solution/new", DraftSolutionCreateView.as_view(), name="draft_solution_new"),
    # Draft edit views
    path("drafts/source/<int:pk>/edit", DraftSourceEditView.as_view(), name="draft_source_edit"),
    path("drafts/source_group/<int:pk>/edit", DraftSourceGroupEditView.as_view(), name="draft_source_group_edit"),
    path("drafts/problem/<int:pk>/edit", DraftProblemEditView.as_view(), name="draft_problem_edit"),
    # Force publish views
    path(
        "drafts/source/<int:pk>/force_publish", DraftSourceForcePublishView.as_view(), name="draft_source_force_publish"
    ),
    path(
        "drafts/source_group/<int:pk>/force_publish",
        DraftSourceGroupForcePublishView.as_view(),
        name="draft_source_group_force_publish",
    ),
    path(
        "drafts/problem/<int:pk>/force_publish",
        DraftProblemForcePublishView.as_view(),
        name="draft_problem_force_publish",
    ),
    path(
        "drafts/solution/<int:pk>/force_publish",
        DraftSolutionForcePublishView.as_view(),
        name="draft_solution_force_publish",
    ),
    # Draft delete views
    path("drafts/source/<int:pk>/delete", DraftSourceDelete.as_view(), name="draft_source_delete"),
    path("drafts/source_group/<int:pk>/delete", DraftSourceGroupDelete.as_view(), name="draft_source_group_delete"),
    path("drafts/problem/<int:pk>/delete", DraftProblemDelete.as_view(), name="draft_problem_delete"),
    path("drafts/source/<int:pk>/delete", DraftSolutionDelete.as_view(), name="draft_solution_delete"),
    # Fork Views
    path("fork/source/<slug:slug>", SourceForkView.as_view(), name="fork_source"),
    path("fork/source_group/<int:pk>", SourceGroupForkView.as_view(), name="fork_source_group"),
    path("fork/problem/<int:pk>", ProblemForkView.as_view(), name="fork_problem"),
    path("fork/solution/<int:pk>", SolutionForkView.as_view(), name="fork_solution"),
]
