from django.contrib import admin

from .models import Problem, Branch, Source, SourceGroup, Technique, Solution, Type

import simple_history


@admin.register(Solution)
class SolutionAdmin(simple_history.admin.SimpleHistoryAdmin):
    list_display = ("pk", "problem", "solution_text")


class SolutionInline(admin.TabularInline):
    model = Solution


@admin.register(Problem)
class ProblemAdmin(simple_history.admin.SimpleHistoryAdmin):
    inlines = [SolutionInline]
    list_display = ("pk", "problem_text", "number", "source", "history")


@admin.register(Source)
class SourceAdmin(simple_history.admin.SimpleHistoryAdmin):
    list_display = (
        "pk",
        "slug",
        "name",
        "shortname",
        "subtitle",
        "problem_count",
        "publish_date",
        "parent",
        "url",
        "history",
    )


@admin.register(SourceGroup)
class SourceGroupAdmin(admin.ModelAdmin):
    list_display = ("pk", "name", "description", "url")


@admin.register(Technique)
class TechniqueAdmin(admin.ModelAdmin):
    list_display = ("pk", "name", "description")


admin.site.register(Branch)
admin.site.register(Type)
