from django.shortcuts import render
from django.views.generic import TemplateView

from problems.models import Problem


class ProblemHistoryView(TemplateView):
    template_name = "history/problem_history.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        history_queryset = None
        if "problem" in context:
            history_queryset = context["problem"].history.all().order_by("history_date")
        else:
            context["problem"] = Problem.history.filter(id=context["pk"]).first()
            history_queryset = Problem.history.filter(id=context["pk"]).order_by(
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

            diffs.append(
                {
                    "history": hist,
                    "diff": diff_value,
                }
            )
            last_hist = hist

        context["diffs"] = diffs

        return context
