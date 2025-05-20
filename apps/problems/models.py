from django.db import models
from django.urls import reverse


class SourceGroup(models.Model):
    """
    A SourceGroup represents an overall Branch for many different sources.
    For example, a math competition occurs every year.
    Individual problems will reference the Source for that years competition.
    That year's competition source will reference a SourceGroup for the overall competition
    """

    name = models.CharField(max_length=128)
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

    name = models.CharField(max_length=128)
    shortname = models.CharField(max_length=40, blank=True, null=True)
    subtitle = models.CharField(max_length=30, blank=True, null=True)
    parent = models.ForeignKey(
        SourceGroup,
        on_delete=models.CASCADE,
        blank=True,
        null=True,
        related_name="sources",
    )
    problem_count = models.PositiveSmallIntegerField(blank=True, null=True)

    description = models.TextField(blank=True, null=True)
    publish_date = models.DateField(blank=True, null=True)
    url = models.URLField(blank=True, null=True)

    class Meta:
        ordering = ["parent", "name"]
        unique_together = ["parent", "shortname", "subtitle"]

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


class Branch(models.Model):
    """
    A Branch represents a branch of mathematics like Calculus or Algebra
    """

    name = models.CharField(max_length=128)
    description = models.TextField(blank=True, null=True)

    class Meta:
        verbose_name_plural = "Branches"

    def __str__(self):
        return self.name[:50]


class Type(models.Model):
    """
    A Type represents the general class of a problem. E.g. Word Problem, Integration
    """

    name = models.CharField(max_length=128)
    description = models.TextField(blank=True, null=True)

    def __str__(self):
        return self.name[:50]


class Technique(models.Model):
    """
    A Technique represents a trick or a book-method for solving a problem
    """

    name = models.CharField(max_length=128)
    description = models.TextField(blank=True)

    def __str__(self):
        return self.name[:50]


class Problem(models.Model):
    """
    A Problem represents the description of a problem, including statement and answer
    """

    problem_text = models.TextField()
    # Having dependency between fields (has_answer and answer_text) doesn't
    # seem normalized. Splitting out to another table would be needlessly
    # complex though.
    has_answer = models.BooleanField(default=False)
    answer_text = models.TextField(blank=True, null=True)

    pub_date = models.DateField(blank=True, null=True)

    # Having dependency between fields (source and number) doesn't
    # seem normalized. Perhaps this should be fixed in the future.
    source = models.ForeignKey(
        Source,
        on_delete=models.CASCADE,
        default=Source.get_default_pk,
        related_name="problems",
    )
    number = models.PositiveSmallIntegerField()
    branches = models.ManyToManyField(Branch, blank=True, related_name="problems")
    types = models.ManyToManyField(Type, blank=True, related_name="problems")

    # Two problems can not share the same problem number and the same source
    class Meta:
        unique_together = ["source", "number"]

    @property
    def techniques(self):
        return Technique.objects.filter(
            pk__in=self.solutions.all().values("techniques")
        )

    def is_published(self):
        return self.pub_date is not None

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


class Solution(models.Model):
    problem = models.ForeignKey(
        Problem, on_delete=models.CASCADE, related_name="solutions"
    )
    techniques = models.ManyToManyField(Technique, blank=True, related_name="solutions")
    solution_text = models.TextField()

    def __str__(self):
        return self.solution_text[:50]

    def get_absolute_url(self):
        return reverse("problem_detail", kwargs={"pk": self.problem.pk})
