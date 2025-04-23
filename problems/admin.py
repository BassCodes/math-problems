from django.contrib import admin

from .models import Problem, Category, Source, SourceGroup, Technique


class ProblemAdmin(admin.ModelAdmin):
    list_display = (
        "problem_text",
        "number",
        "source",
        "contributor",
    )


class SourceAdmin(admin.ModelAdmin):
    list_display = ("name", "shortname", "subtitle", "publish_date", "parent", "url")


class SourceGroupAdmin(admin.ModelAdmin):
    list_display = ("name", "description", "url")


class TechniqueAdmin(admin.ModelAdmin):
    list_display = ("name", "description")


admin.site.register(Problem, ProblemAdmin)
admin.site.register(Category)
admin.site.register(SourceGroup, SourceGroupAdmin)
admin.site.register(Source, SourceAdmin)
admin.site.register(Technique, TechniqueAdmin)
