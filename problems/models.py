from django.db import models
from django.urls import reverse


class SourceGroup(models.Model):
    """
    A SourceGroup represents an overall category for many different sources.
    For example, a math competition occurs every year.
    Individual problems will reference the Source for that years competition.
    That year's competition source will reference a SourceGroup for the overall competition
    """

    name = models.TextField()
    description = models.TextField(blank=True, null=True)
    url = models.URLField(blank=True, null=True)

    def __str__(self):
        return self.name[:50]

    def get_absolute_url(self):
        return reverse("source_group_detail", kwargs={"pk": self.pk})


class Source(models.Model):
    """
    A Source represents a single 'document' containing many math problems
    """

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

    class Meta:
        ordering = ["parent", "name"]

    # Source https://stackoverflow.com/a/62697872
    @classmethod
    def get_default_pk(cls):
        source, created = cls.objects.get_or_create(
            name="Assorted",
        )
        return source.pk

    def get_problems(self):
        return self.problems.order_by("number")

    def __str__(self):
        if self.subtitle:
            return f"{self.name}  {self.subtitle}"
        else:
            return self.name

    def full_name(self):
        return self.__str__()

    def get_short_name(self):
        if self.shortname:
            if self.subtitle:
                return f"{self.shortname}  {self.subtitle}"
            else:
                return self.shortname
        else:
            return self.full_name()

    def get_absolute_url(self):
        return reverse("source_detail", kwargs={"pk": self.pk})


class Category(models.Model):
    """
    A category represents a branch of mathematics like Calculus or Algebra
    """

    name = models.TextField()
    description = models.TextField(blank=True, null=True)

    class Meta:
        verbose_name_plural = "Categories"

    def __str__(self):
        return self.name[:50]


class Technique(models.Model):
    """
    A Technique represents a trick or a book-method for solving a problem
    """

    name = models.TextField()
    description = models.TextField(blank=True)

    def __str__(self):
        return self.name[:50]


class Problem(models.Model):
    """
    A Problem represents the entire description of a problem, including statement, solution, and answer
    """

    problem_text = models.TextField()
    solution_text = models.TextField()
    answer_text = models.TextField()

    contributor = models.ForeignKey(
        "accounts.CustomUser",
        on_delete=models.CASCADE,
    )

    pub_date = models.DateField(blank=True, null=True)

    source = models.ForeignKey(
        Source,
        on_delete=models.CASCADE,
        default=Source.get_default_pk,
        related_name="problems",
    )
    number = models.PositiveSmallIntegerField(blank=True, null=True)
    categories = models.ManyToManyField(Category, blank=True, related_name="problems")
    techniques = models.ManyToManyField(Technique, blank=True, related_name="problems")

    # Two problems can not share the same problem number and the same source
    class Meta:
        unique_together = ("source", "number")

    def get_next(self):
        if self.source is None:
            return None

        if self.number:
            next_problem = (
                Problem.objects.order_by("number")
                .filter(source_id=self.source.pk, number__gt=self.number)
                .first()
            )
            return next_problem
        else:
            return None

    def get_prev(self):
        if self.source is None:
            return None

        if self.number:
            prev_problem = (
                Problem.objects.order_by("number")
                .filter(source_id=self.source.pk, number__lt=self.number)
                .last()
            )
            return prev_problem
        else:
            return None

    def __str__(self):
        return self.problem_text[:50]

    def get_absolute_url(self):
        return reverse("problem_detail", kwargs={"pk": self.pk})

    def is_published(self):
        return self.pub_date is not None
