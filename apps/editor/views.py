from django.views.generic import (
    TemplateView,
    CreateView,
    UpdateView,
    DeleteView,
    DetailView,
)
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.contrib.auth.decorators import login_required, permission_required
from django.urls import reverse_lazy
from django.db.models import F, Count
from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.core.exceptions import ObjectDoesNotExist

from .forms import ProblemForm, SolutionForm, SourceForm

import accounts

import datetime
import problems
from .models import DraftProblem, DraftSource, DraftRef


class EditorHomePageView(LoginRequiredMixin, TemplateView):
    template_name = "editor/editor_home.html"


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
@permission_required("problems.add_problem")
def problem_create_view(request):
    # Todo add drafts/publishing
    if request.method == "POST":
        problem_form = ProblemForm(
            request.POST, instance=problems.models.Problem(), prefix="prb"
        )
        solution_form = SolutionForm(
            request.POST, instance=problems.models.Solution(), prefix="sol"
        )
        if problem_form.is_valid() and solution_form.is_valid():
            new_problem = problem_form.save(commit=False)
            new_problem.contributor = request.user
            new_problem.pub_date = datetime.date.today()
            new_problem.save()

            new_solution = solution_form.save(commit=False)
            new_solution.problem = new_problem
            new_solution.save()
            return HttpResponseRedirect(new_problem.get_absolute_url())
    else:
        specified_source_pk = request.GET.get("src")
        specified_problem_no = request.GET.get("no")
        prob_inst = problems.models.Problem()
        if specified_source_pk and specified_problem_no:
            prob_inst.source = problems.models.Source.objects.get(
                pk=specified_source_pk
            )
            prob_inst.number = specified_problem_no

        problem_form = ProblemForm(instance=prob_inst, prefix="prb")
        solution_form = SolutionForm(instance=problems.models.Solution(), prefix="sol")
    return render(
        request,
        "editor/problem_create.html",
        {"problem_form": problem_form, "solution_form": solution_form},
    )


@login_required
@permission_required("problems.change_problem")
def problem_update_view(request, pk):
    # Todo add drafts/publishing
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
            solution_forms.append(
                SolutionForm(
                    request.POST, instance=problems.models.Solution(), prefix=f"sol{i}"
                )
            )

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
    dummy_solution_form = SolutionForm(
        instance=problems.models.Solution(), prefix="solREPLACEME"
    )
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


class EditorProblemDeleteView(LoginRequiredMixin, PermissionRequiredMixin, DeleteView):
    permission_required = "problems.delete_problem"
    model = problems.models.Problem
    template_name = "editor/problem_confirm_delete.html"
    success_url = reverse_lazy("editor_home")


class SolutionDeleteView(LoginRequiredMixin, PermissionRequiredMixin, DeleteView):
    model = problems.models.Solution
    permission_required = "problems.delete_problem"

    template_name = "editor/solution_delete.html"

    # Redirect to problem page
    def get_success_url(self, **kwargs):
        parent_id = self.get_object().problem.id
        return reverse_lazy("problem_detail", kwargs={"pk": parent_id})


class SourceEditView(LoginRequiredMixin, PermissionRequiredMixin, UpdateView):
    model = problems.models.Source
    permission_required = "problems.change_source"
    fields = [
        "name",
        "shortname",
        "subtitle",
        "parent",
        "problem_count",
        "description",
        "publish_date",
        "url",
    ]
    template_name = "editor/source_edit.html"


# @login_required
# def source_create_draft_view(
#     request,
#     draft_id,
# ):
#     problem = problems.models.Problem.objects.get(id=d)

#     if request.method == "POST":
#         problem_form = ProblemForm(request.POST, instance=problem, prefix="prb")

#         highest_solution = problem.solutions.count()
#         additional_solutions = int(request.POST.get("additional_solutions", 0))
#         solution_forms = [
#             SolutionForm(request.POST, instance=solution, prefix=f"sol{i}")
#             for (i, solution) in enumerate(problem.solutions.all())
#         ]
#         for i in range(highest_solution, highest_solution + additional_solutions):
#             solution_forms.append(
#                 SolutionForm(
#                     request.POST, instance=problems.models.Solution(), prefix=f"sol{i}"
#                 )
#             )

#         if problem_form.is_valid() and all([s.is_valid() for s in solution_forms]):
#             problem_form.save(commit=True)

#             for solution_form in solution_forms:
#                 new_solution = solution_form.save(commit=False)
#                 new_solution.problem = problem
#                 new_solution.save()

#             return HttpResponseRedirect(problem.get_absolute_url())
#     else:
#         problem_form = ProblemForm(instance=problem, prefix="prb")
#         solution_forms = []
#         for i, solution in enumerate(problem.solutions.all()):
#             solution_form = SolutionForm(instance=solution, prefix=f"sol{i}")
#             solution_form.x_form_no = i
#             solution_forms.append(solution_form)

#     # Dummy solution form. used as a template create additional solutions for the problem
#     dummy_solution_form = SolutionForm(
#         instance=problems.models.Solution(), prefix="solREPLACEME"
#     )
#     return render(
#         request,
#         "editor/problem_edit.html",
#         {
#             "problem": problem,
#             "problem_form": problem_form,
#             "solution_forms": solution_forms,
#             "dummy_solution": dummy_solution_form,
#         },
#     )


class SourceCreateView(LoginRequiredMixin, PermissionRequiredMixin, CreateView):
    model = DraftSource
    permission_required = "problems.add_source"
    fields = [
        "name",
        "shortname",
        "subtitle",
        "parent",
        "problem_count",
        "description",
        "publish_date",
        "url",
    ]
    template_name = "editor/source_create.html"
    success_url = reverse_lazy("editor_home")

    def form_valid(self, form):
        return super().form_valid(form)

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


class SourceGroupEditView(LoginRequiredMixin, PermissionRequiredMixin, UpdateView):
    model = problems.models.SourceGroup
    permission_required = "problems.change_sourcegroup"
    fields = [
        "name",
        "description",
        "url",
    ]
    template_name = "editor/sourcegroup_edit.html"
    success_url = reverse_lazy("editor_home")


class SourceGroupCreateView(LoginRequiredMixin, PermissionRequiredMixin, CreateView):
    model = problems.models.SourceGroup
    permission_required = "problems.add_sourcegroup"
    fields = [
        "name",
        "description",
        "url",
    ]
    template_name = "editor/sourcegroup_create.html"
    success_url = reverse_lazy("editor_home")


# TODO Auth
class UserDraftsDetailView(DetailView):
    model = accounts.models.CustomUser
    template_name = "editor/user_drafts.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["draft_sources"] = DraftSource.objects.owned_by(self.request.user)
        context["draft_source_groups"] = DraftProblem.objects.owned_by(
            self.request.user
        )
        context["draft_problems"] = DraftProblem.objects.owned_by(self.request.user)
        context["draft_solutions"] = DraftProblem.objects.owned_by(self.request.user)
        return context
