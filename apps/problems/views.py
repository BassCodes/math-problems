from django.shortcuts import render
from django.views.generic import TemplateView, ListView, DetailView
from django.db.models import Q
from django.shortcuts import get_object_or_404
from django.http import HttpResponseForbidden
from django.contrib.auth.mixins import LoginRequiredMixin

from django.core.paginator import Paginator
from .models import Problem, Source, SourceGroup, Solution, Technique, Branch, Type
from .forms import SearchForm


class HomePageView(TemplateView):
    template_name = "home.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["newest_problems"] = (
            Problem.objects.all()
            # .order_by("pub_date")
            .reverse()[:3]
        )
        return context


def problem_list_view(request):
    search_form = SearchForm(request.GET)

    query = Q()
    solution_query = Q()

    filter_by_solution = False
    if search_form.is_valid():
        source_query = Q()
        for source in search_form.cleaned_data["source"]:
            source_query |= Q(source__exact=source.id)
        query &= source_query

        branch_query = Q()
        for branch in search_form.cleaned_data["branch"]:
            branch_query &= Q(branches__exact=branch.id)
        query &= branch_query

        type_query = Q()
        for type in search_form.cleaned_data["type"]:
            type_query |= ~Q(types__id=type.id)
        query &= ~type_query

        if search_form.cleaned_data["tech"]:
            technique_query = Q()
            filter_by_solution = True

            for technique in search_form.cleaned_data["tech"]:
                technique_query |= ~Q(techniques__id=technique.id)

            solution_query &= ~technique_query

    context = {}

    if filter_by_solution:
        # The filter_by_solution enables filtering the set of problems by a set of solutions.
        # If filtering by solution is not needed, this cuts down on an extra database query.
        solutions = Solution.objects.filter(solution_query)
        context["problems"] = (
            Problem.objects.filter(query)
            .filter(solutions__in=solutions)
            .order_by("source", "number")
        )
    else:
        # Also, without this branch, a bug arises when problems have no
        # solutions. Without the branch those problems would simply be lost.
        context["problems"] = (
            Problem.objects.prefetch_related("source")
            .filter(query)
            .order_by("source", "number")
        )

    context["search_form"] = search_form

    return render(request, "problem_list.html", context)


def problem_detail_view(request, slug, number):
    problem = get_object_or_404(Problem, source__slug=slug, number=number)

    context = {}
    context["problem"] = problem
    return render(request, "problem.html", context)


class SourceListView(ListView):
    model = Source
    template_name = "source_list.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["source_list"] = Source.objects.all().order_by("parent").reverse()
        return context


class SourceDetailView(DetailView):
    model = Source
    template_name = "source.html"


class SourceGroupDetailView(DetailView):
    model = SourceGroup
    template_name = "source_group.html"


class SourceMissingProblemsView(DetailView):
    template_name = "source_missing_problems.html"
    model = Source

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        source = context["source"]

        numbered_problems = {}

        p = source.problems.all()
        for problem in p:
            numbered_problems[problem.number] = problem

        ordered_problems_and_blanks = []

        if source.problem_count:
            max_problems = source.problem_count
        elif source.problems.all().count() != 0:
            max_problems = source.problems.all().order_by("number").last().number
        else:
            return context

        for num in range(1, max_problems + 1):
            if num in numbered_problems:
                ordered_problems_and_blanks.append(numbered_problems[num])
            else:
                ordered_problems_and_blanks.append(None)
        context["problems"] = ordered_problems_and_blanks

        return context


def tags_view(request):
    context = {}
    context["techniques"] = Technique.objects.all().order_by("name")
    context["types"] = Type.objects.all().order_by("name")
    context["branches"] = Branch.objects.all().order_by("name")
    return render(request, "tag_listing.html", context)
