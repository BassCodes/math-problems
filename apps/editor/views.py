from django.views.generic import (
    TemplateView,
    DetailView,
)
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.decorators import login_required, permission_required
from django.db.models import F, Count
from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.core.exceptions import ObjectDoesNotExist

import accounts
import problems

from .models import DraftProblem, DraftSource, DraftSourceGroup, DraftSolution, DraftRef
from .forms import ProblemForm, SolutionForm


from .view_factories import (
    draft_create_view_factory,
    draft_delete_view_factory,
    draft_detail_view_factory,
    draft_edit_view_factory,
    draft_force_publish_factory,
    fork_factory,
)


class IncompleteSourceView(LoginRequiredMixin, TemplateView):
    template_name = "editor/sources_incomplete.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["sources"] = (
            problems.models.Source.objects.all()
            .filter(problem_count__isnull=False)
            .annotate(existing_problem_count=Count("problems"))
            .filter(existing_problem_count__lt=F("problem_count"))
            .order_by("parent")
        )
        return context


@login_required
@permission_required("problems.change_problem")
def problem_update_view(request, pk):
    problem = problems.models.Problem.objects.get(id=pk)

    if request.method == "POST":
        problem_form = ProblemForm(request.POST, instance=problem, prefix="prb")

        highest_solution = problem.solutions.count()
        additional_solutions = int(request.POST.get("additional_solutions", 0))
        solution_forms = [
            SolutionForm(request.POST, instance=solution, prefix=f"sol{i}")
            for (i, solution) in enumerate(problem.solutions.all())
        ]
        for i in range(highest_solution, highest_solution + additional_solutions):
            solution_forms.append(SolutionForm(request.POST, instance=problems.models.Solution(), prefix=f"sol{i}"))

        if problem_form.is_valid() and all([s.is_valid() for s in solution_forms]):
            problem_form.save(commit=True)

            for solution_form in solution_forms:
                new_solution = solution_form.save(commit=False)
                new_solution.problem = problem
                new_solution.save()

            return HttpResponseRedirect(problem.get_absolute_url())
    else:
        problem_form = ProblemForm(instance=problem, prefix="prb")
        solution_forms = []
        for i, solution in enumerate(problem.solutions.all()):
            solution_form = SolutionForm(instance=solution, prefix=f"sol{i}")
            solution_form.x_form_no = i
            solution_forms.append(solution_form)

    # Dummy solution form. used as a template create additional solutions for the problem
    dummy_solution_form = SolutionForm(instance=problems.models.Solution(), prefix="solREPLACEME")
    return render(
        request,
        "editor/problem_edit.html",
        {
            "problem": problem,
            "problem_form": problem_form,
            "solution_forms": solution_forms,
            "dummy_solution": dummy_solution_form,
        },
    )


# TODO Auth
class UserDraftsDetailView(LoginRequiredMixin, DetailView):
    model = accounts.models.CustomUser
    template_name = "editor/user_drafts.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["draft_sources"] = DraftSource.objects.owned_by(self.request.user)
        context["draft_source_groups"] = DraftSourceGroup.objects.owned_by(self.request.user)
        context["draft_problems"] = DraftProblem.objects.owned_by(self.request.user)
        return context


class MyDraftsDetailView(LoginRequiredMixin, DetailView):
    model = accounts.models.CustomUser
    template_name = "editor/user_drafts.html"

    def get_object(self):
        return self.request.user

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["draft_sources"] = DraftSource.objects.owned_by(self.request.user)
        context["draft_source_groups"] = DraftSourceGroup.objects.owned_by(self.request.user)
        context["draft_problems"] = DraftProblem.objects.owned_by(self.request.user)
        return context


SourceForkView = fork_factory(problems.models.Source, DraftSource)
SourceGroupForkView = fork_factory(problems.models.SourceGroup, DraftSourceGroup)
ProblemForkView = fork_factory(problems.models.Problem, DraftProblem)
SolutionForkView = fork_factory(problems.models.Solution, DraftSolution)

DraftSourceForcePublishView = draft_force_publish_factory(DraftSource)
DraftSourceGroupForcePublishView = draft_force_publish_factory(DraftSourceGroup)
DraftProblemForcePublishView = draft_force_publish_factory(DraftProblem)
DraftSolutionForcePublishView = draft_force_publish_factory(DraftSolution)

DraftSourceDelete = draft_delete_view_factory(DraftSource)
DraftSourceGroupDelete = draft_delete_view_factory(DraftSourceGroup)
DraftSolutionDelete = draft_delete_view_factory(DraftSolution)
DraftProblemDelete = draft_delete_view_factory(DraftProblem)


DraftSourceGroupEditView = draft_edit_view_factory(
    DraftSourceGroup,
    [
        "name",
        "description",
        "url",
    ],
)
DraftProblemEditView = draft_edit_view_factory(
    DraftProblem,
    ["problem_text", "has_answer", "answer_text", "source", "draft_source", "number"],
)
DraftSourceEditView = draft_edit_view_factory(
    DraftSource,
    [
        "name",
        "slug",
        "shortname",
        "subtitle",
        "parent",
        "draft_parent",
        "problem_count",
        "description",
        "publish_date",
        "url",
    ],
)


DraftSourceView = draft_detail_view_factory(DraftSource, "source.html", "source")
DraftSourceGroupView = draft_detail_view_factory(DraftSourceGroup, "source_group.html", "sourcegroup")
DraftProblemView = draft_detail_view_factory(DraftProblem, "problem.html", "problem")


DraftSourceGroupCreateView = draft_create_view_factory(
    DraftSourceGroup,
    [
        "name",
        "description",
        "url",
    ],
)
DraftProblemCreateView = draft_create_view_factory(
    DraftProblem,
    [
        "problem_text",
        "has_answer",
        "answer_text",
        "source",
        "draft_source",
        "number",
    ],
)
DraftSolutionCreateView = draft_create_view_factory(
    DraftSolution,
    [
        "solution_text",
        "problem",
        "draft_problem",
    ],
)
DraftSourceCreateView = draft_create_view_factory(
    DraftSource,
    [
        "name",
        "shortname",
        "subtitle",
        "parent",
        "draft_parent",
        "problem_count",
        "description",
        "publish_date",
        "url",
    ],
)


def get_initial(self):
    # Get URL parameters for specific SourceGroup and select that SourceGroup
    specified_group_id = self.request.GET.get("group")
    if specified_group_id:
        try:
            parent = problems.models.SourceGroup.objects.get(pk=specified_group_id)
            if parent:
                return {"parent": parent}
        except ObjectDoesNotExist:
            return {}

    return {}


DraftSourceCreateView.get_initial = get_initial
