from django.shortcuts import render
from django.views.generic import TemplateView

from problems.models import Problem, Solution, Source


class ProblemHistoryView(TemplateView):
    template_name = "history/problem_history.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        history_queryset = None
        # When a problem is deleted, the problem object can not be found from
        context["problem"] = Problem.objects.get(id=context["pk"])
        if context["problem"]:
            history_queryset = context["problem"].history.all().order_by("history_date")
        else:
            context["problem"] = Problem.history.filter(id=context["pk"]).first()
            history_queryset = Problem.history.filter(id=context["pk"]).order_by(
                "history_date"
            )

        diffs = []
        last_hist = None
        for hist in history_queryset:
            solutions_modified = Solution.history.all().filter(
                history_problem_ref_id=hist.history_id
            )
            diff_value = None
            if last_hist:
                diff_value = last_hist.diff_against(hist)
                if not diff_value.changed_fields:
                    diff_value = None

            diffs.append(
                {"history": hist, "diff": diff_value, "solutions": solutions_modified}
            )
            last_hist = hist

        context["diffs"] = diffs

        return context


class SourceHistoryView(TemplateView):
    template_name = "history/problem_history.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        history_queryset = None
        # When a problem is deleted, the problem object can not be found from
        context["source"] = Source.objects.get(slug=context["slug"])
        if context["source"]:
            history_queryset = context["source"].history.all().order_by("history_date")
        else:
            context["source"] = Source.history.filter(slug=context["slug"]).first()
            history_queryset = Source.history.filter(slug=context["slug"]).order_by(
                "history_date"
            )

        diffs = []
        last_hist = None
        for hist in history_queryset:
            diff_value = None
            if last_hist:
                diff_value = last_hist.diff_against(hist)
                if not diff_value.changed_fields:
                    diff_value = None

            diffs.append({"history": hist, "diff": diff_value})
            last_hist = hist

        context["diffs"] = diffs

        return context
