from django.contrib import admin

from .models import Problem, Branch, Source, SourceGroup, Technique, Solution, Type


class SolutionInline(admin.TabularInline):
    model = Solution


class ProblemAdmin(admin.ModelAdmin):
    inlines = [SolutionInline]
    list_display = ("pk", "problem_text", "number", "source", "pub_date")


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


class SourceGroupAdmin(admin.ModelAdmin):
    list_display = ("pk", "name", "description", "url")


class TechniqueAdmin(admin.ModelAdmin):
    list_display = ("pk", "name", "description")


class SolutionAdmin(admin.ModelAdmin):
    list_display = ("pk", "problem", "solution_text")


admin.site.register(Problem, ProblemAdmin)
admin.site.register(Branch)
admin.site.register(Type)
admin.site.register(Solution, SolutionAdmin)
admin.site.register(SourceGroup, SourceGroupAdmin)
admin.site.register(Source, SourceAdmin)
admin.site.register(Technique, TechniqueAdmin)
