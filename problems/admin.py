from django.contrib import admin

from .models import Problem, Branch, Source, SourceGroup, Technique, Solution, Type


@admin.register(Solution)
class SolutionAdmin(admin.ModelAdmin):
    list_display = ("pk", "problem", "solution_text")


class SolutionInline(admin.TabularInline):
    model = Solution


@admin.register(Problem)
class ProblemAdmin(admin.ModelAdmin):
    inlines = [SolutionInline]
    list_display = ("pk", "problem_text", "number", "source", "pub_date")


@admin.register(Source)
class SourceAdmin(admin.ModelAdmin):
    list_display = (
        "pk",
        "name",
        "shortname",
        "subtitle",
        "problem_count",
        "publish_date",
        "parent",
        "url",
    )


@admin.register(SourceGroup)
class SourceGroupAdmin(admin.ModelAdmin):
    list_display = ("pk", "name", "description", "url")


@admin.register(Technique)
class TechniqueAdmin(admin.ModelAdmin):
    list_display = ("pk", "name", "description")


admin.site.register(Branch)
admin.site.register(Type)
