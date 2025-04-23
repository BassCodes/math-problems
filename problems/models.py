from django.db import models
from django.urls import reverse


# A SourceGroup represents an overall category for many different sources.
# For example, a math competition occurs every year.
# Individual problems will reference the Source for that years competition.
# That year's competition source will reference a SourceGroup for the overall competition
class SourceGroup(models.Model):
    name = models.TextField()
    description = models.TextField(blank=True, null=True)
    url = models.URLField(blank=True, null=True)

    def __str__(self):
        return self.name[:50]

    def get_absolute_url(self):
        return reverse("source_group_detail", kwargs={"pk": self.pk})


# A Source represents a single 'document' containing many math problems
class Source(models.Model):
    name = models.TextField()
    shortname = models.TextField(blank=True, null=True)
    subtitle = models.TextField(blank=True, null=True)
    parent = models.ForeignKey(
        SourceGroup,
        on_delete=models.CASCADE,
        blank=True,
        null=True,
        related_name="sources",
    )
    description = models.TextField(blank=True, null=True)
    publish_date = models.DateField(blank=True, null=True)
    url = models.URLField(blank=True, null=True)

    def __str__(self):
        return self.name[:50] + " " + str(self.publish_date)

    def get_absolute_url(self):
        return reverse("source_detail", kwargs={"pk": self.pk})


class Category(models.Model):
    name = models.TextField()
    description = models.TextField(blank=True, null=True)

    class Meta:
        verbose_name_plural = "Categories"

    def __str__(self):
        return self.name[:50]


class Technique(models.Model):
    name = models.TextField()
    description = models.TextField(blank=True)

    def __str__(self):
        return self.name[:50]


class Problem(models.Model):
    problem_text = models.TextField()
    solution_text = models.TextField()
    answer_text = models.TextField()

    contributor = models.ForeignKey(
        "auth.User",
        on_delete=models.CASCADE,
    )

    source = models.ForeignKey(
        Source, on_delete=models.CASCADE, related_name="problems"
    )
    number = models.PositiveSmallIntegerField()
    categories = models.ManyToManyField(Category, blank=True, related_name="problems")
    techniques = models.ManyToManyField(Technique, blank=True, related_name="problems")

    # Two problems can not share the same problem number and the same source
    class Meta:
        unique_together = ("source", "number")

    def get_next(self):
        if self.source is None:
            return None

        if self.number:
            next_problem = Problem.objects.filter(
                source_id=self.source.pk, number__gt=self.number
            ).first()
            return next_problem
        else:
            return None

    def get_prev(self):
        if self.source is None:
            return None

        if self.number:
            prev_problem = Problem.objects.filter(
                source_id=self.source.pk, number__lt=self.number
            ).first()
            return prev_problem
        else:
            return None

    def get_problems_of_same_source(self):
        if self.source:
            return Problem.objects.filter(source_id=self.source.pk)
        else:
            return None

    def __str__(self):
        return self.problem_text[:50]

    def get_absolute_url(self):
        return reverse("problem_detail", kwargs={"pk": self.pk})
