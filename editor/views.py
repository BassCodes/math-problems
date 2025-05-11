from django.views.generic import (
    TemplateView,
    CreateView,
    UpdateView,
    DeleteView,
    DetailView,
)
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.decorators import login_required
from django.urls import reverse_lazy
from django.db.models import Q, F, Count
from django.http import HttpResponseRedirect
from django.shortcuts import render
from .forms import ProblemForm, SolutionForm
from django.views.generic.edit import FormView


import datetime
import problems


class EditorHomePageView(LoginRequiredMixin, TemplateView):
    template_name = "editor/editor_home.html"


class EditorMissingProblemsView(LoginRequiredMixin, TemplateView):
    template_name = "editor/missing_problems.html"

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


class EditorIncompleteSourceView(LoginRequiredMixin, DetailView):
    template_name = "editor/incomplete_source.html"
    model = problems.models.Source

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        source = context["source"]

        numbered_problems = {}

        p = source.problems.all()
        for problem in p:
            numbered_problems[problem.number] = problem

        ordered_problems_and_blanks = []
        for num in range(1, source.problem_count + 1):
            if num in numbered_problems:
                ordered_problems_and_blanks.append(numbered_problems[num])
            else:
                ordered_problems_and_blanks.append(None)
        context["listicle"] = ordered_problems_and_blanks

        return context


@login_required
def problem_create_view(request):
    # TODO authenticate
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
            new_problem.pub_date = pub_date = datetime.date.today()
            new_problem.save()

            new_solution = solution_form.save(commit=False)
            new_solution.problem = new_problem
            new_solution.save()
            return HttpResponseRedirect(
                reverse_lazy("problem_detail", kwargs={"pk": new_problem.pk})
            )
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
        "editor/create_problem.html",
        {"problem_form": problem_form, "solution_form": solution_form},
    )


@login_required
def problem_update_view(request, pk):
    # TODO authenticate
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
                print(solution_form.data)
                new_solution = solution_form.save(commit=False)
                new_solution.problem = problem
                new_solution.save()

            return HttpResponseRedirect(
                reverse_lazy("problem_detail", kwargs={"pk": pk})
            )
    else:
        problem_form = ProblemForm(instance=problem, prefix="prb")
        solution_forms = []
        for i, solution in enumerate(problem.solutions.all()):
            solution_form = SolutionForm(instance=solution, prefix=f"sol{i}")
            solution_form.x_form_no = i
            solution_forms.append(solution_form)

    # Dummy solution form. used as a template create additional solutions for the problem
    dummy_solution_form = SolutionForm(instance=problems.models.Solution())
    return render(
        request,
        "editor/edit_problem.html",
        {
            "problem_form": problem_form,
            "solution_forms": solution_forms,
            "dummy_solution": dummy_solution_form,
        },
    )


class EditorUpdateProblemView(LoginRequiredMixin, UpdateView):
    model = problems.models.Problem
    template_name = "editor/edit_problem.html"
    fields = (
        "problem_text",
        "answer_text",
        "source",
        "number",
        "categories",
    )


class EditorProblemDeleteView(LoginRequiredMixin, DeleteView):
    model = problems.models.Problem
    template_name = "editor/problem_confirm_delete.html"
    success_url = reverse_lazy("editor_home")
