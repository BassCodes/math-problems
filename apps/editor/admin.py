from django.contrib import admin

from .models import DraftProblem, DraftSource


@admin.register(DraftProblem)
class DraftProblemAdmin(admin.ModelAdmin):
    list_display = (
        "pk",
        "problem_text",
        "has_answer",
        "answer_text",
        "source",
        "draft_source",
        "number",
    )


@admin.register(DraftSource)
class DraftSourceAdmin(admin.ModelAdmin):
    list_display = (
        "pk",
        "slug",
        "name",
        "shortname",
        "subtitle",
        "parent",
        "draft_parent",
        "problem_count",
        "description",
        "publish_date",
        "url",
    )
