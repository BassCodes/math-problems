from django import template

register = template.Library()


@register.inclusion_tag("partials/problem_list.html")
def problem_list(problems, **kwargs):
    context = {"problems": problems}

    if "ord" in kwargs:
        context["ordered"] = True
        del kwargs["ord"]

    for key, value in kwargs.items():
        raise KeyError(
            f"While rendering problem list: unknown parameters ({key}, {value})"
        )

    return context
