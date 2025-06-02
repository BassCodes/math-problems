from django.contrib import admin

from .models import DraftProblem, DraftSource, DraftSourceGroup, DraftSolution, DraftRef


@admin.register(DraftRef)
class DraftRefAdmin(admin.ModelAdmin):
    list_display = ("pk", "draft_owner", "draft_created", "draft_edited", "draft_state")


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


@admin.register(DraftSourceGroup)
class SourceGroupAdmin(admin.ModelAdmin):
    list_display = ("pk", "name", "description", "url")


@admin.register(DraftSolution)
class SolutionAdmin(admin.ModelAdmin):
    list_display = ("pk", "problem", "draft_problem", "solution_text")
