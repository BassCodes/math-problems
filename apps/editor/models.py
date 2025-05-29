from django.db import models
from django.urls import reverse
from simple_history.models import HistoricalRecords

from django.contrib.contenttypes.fields import GenericForeignKey, GenericRelation
from django.contrib.contenttypes.models import ContentType

from problems.models import Source, SourceGroup, Problem
from accounts.models import CustomUser


class DraftRef(models.Model):
    class DraftState(models.TextChoices):
        DRAFT = ("DR", "Draft")
        IN_REVIEW = ("RE", "In Review")

    draft_owner = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    draft_created = models.DateTimeField(auto_now=True)
    draft_edited = models.DateTimeField(auto_now_add=True)
    draft_state = models.CharField(
        max_length=2, choices=DraftState, default=DraftState.DRAFT
    )
    content_type = models.ForeignKey(
        ContentType, on_delete=models.CASCADE, related_name="bbbbb"
    )
    object_id = models.PositiveIntegerField()
    content_object = GenericForeignKey("content_type", "object_id")

    forked_object_id = models.PositiveIntegerField(null=True)
    forked_content_type = models.ForeignKey(
        ContentType, on_delete=models.CASCADE, related_name="aaaaa", null=True
    )
    forked_content_object = GenericForeignKey("forked_content_type", "forked_object_id")

    class Meta:
        unique_together = ("content_type", "object_id")

    @classmethod
    def create_new(cls, user, draft_instance, forked_from=None):
        ctype = ContentType.objects.get_for_model(draft_instance.__class__)
        new_draft_ref = cls.objects.create(
            content_type=ctype, content_object=draft_instance, draft_owner=user
        )
        if forked_from is not None:
            forked_ctype = ContentType.objects.get_for_model(forked_from.__class__)
            new_draft_ref.forked_content_type = forked_ctype
            new_draft_ref.forked_content_object = forked_from
        return new_draft_ref


class DraftableMetaclass(type):
    def __new__(cls, clsname, bases, attrs):
        uppercase_attrs = {
            attr if attr.startswith("__") else attr.upper(): v
            for attr, v in attrs.items()
        }
        attrs["forked_object"] = models.ForeignKey(
            attrs["DraftMeta"].for_class,
            on_delete=models.SET_NULL,
            null=True,
            blank=True,
        )
        return type(clsname, bases, uppercase_attrs)


class Draftable(
    models.Model,
):
    class Meta:
        abstract = True

    class DraftMeta:
        for_class = "TO BE OVERWRITTEN"

    draft_ref = GenericRelation(
        DraftRef, content_type_field="content_type", object_id_field="object_id"
    )

    @classmethod
    def get_meta_class_model(cls):
        # TODO assert is class
        return cls.DraftMeta.for_class

    @classmethod
    def create_new(cls, user, forked_from=None, **kwargs):
        if forked_from is not None:
            obj = cls.create_from_published(forked_from)
        else:
            obj = cls.objects.create(**kwargs)
        draft_ref = DraftRef.create_new(user, obj, forked_from=forked_from)
        obj.save()
        draft_ref.save()
        return obj

    def get_draft_ref(self):
        return self.draft_ref.first()

    def send_to_review(self):
        ref = self.get_draft_ref()
        assert ref.draft_state == DraftRef.DraftState.DRAFT
        ref.draft_state = DraftRef.DraftState.IN_REVIEW
        ref.save()

    def send_back_to_draft(self):
        ref = self.get_draft_ref()
        assert ref.draft_state == DraftRef.DraftState.IN_REVIEW
        ref.draft_state = DraftRef.DraftState.DRAFT
        ref.save()

    def publish(self):
        ref = self.get_draft_ref()
        assert ref.draft_state == DraftRef.DraftState.IN_REVIEW

        converted = self.convert_to_published(ref.forked_content_object)
        converted.save()
        self.delete()
        return converted

    def get_forked_object(self):
        return self.get_draft_ref().forked_content_object

    def is_fork(self):
        return self.get_forked_object() is not None


class DraftSourceGroup(Draftable, models.Model):
    name = models.CharField(max_length=128, blank=True, null=True)
    description = models.TextField(blank=True, null=True)
    url = models.URLField(blank=True, null=True)

    @classmethod
    def create_from_published(cls, published):
        obj = cls.objects.create()
        obj.name = published.name
        obj.description = published.description
        obj.url = published.url
        return obj

    def convert_to_published(self, existing=None):
        if existing is None:
            published = SourceGroup()
        else:
            published = existing

        published.name = self.name
        published.description = self.description
        published.url = self.url
        published.save()
        # Find DraftProblem which depend upon this and convert their `draft_source` to `source`
        dependents = DraftSource.objects.filter(draft_parent=self)

        for dep in dependents:
            dep.draft_parent = None
            dep.parent = published
            dep.save()

        return published


class DraftSource(Draftable, models.Model):
    slug = models.SlugField(max_length=50, blank=True, null=True)
    name = models.CharField(max_length=128, blank=True, null=True)
    shortname = models.CharField(max_length=40, blank=True, null=True)
    subtitle = models.CharField(max_length=30, blank=True, null=True)
    parent = models.ForeignKey(
        SourceGroup,
        on_delete=models.SET_NULL,
        blank=True,
        null=True,
    )
    draft_parent = models.ForeignKey(
        DraftSourceGroup,
        on_delete=models.SET_NULL,
        blank=True,
        null=True,
    )
    problem_count = models.PositiveSmallIntegerField(blank=True, null=True)

    description = models.TextField(blank=True, null=True)
    publish_date = models.DateField(blank=True, null=True)
    url = models.URLField(blank=True, null=True)

    @classmethod
    def create_from_published(cls, published):
        obj = cls.objects.create()
        obj.slug = published.slug
        obj.name = published.name
        obj.shortname = published.shortname
        obj.subtitle = published.subtitle
        obj.parent = published.parent
        obj.problem_count = published.problem_count
        obj.url = published.url
        return obj

    def convert_to_published(self, existing=None):
        if existing is None:
            published = Source()
        else:
            published = existing

        published.slug = self.slug
        published.name = self.name
        published.shortname = self.shortname
        published.subtitle = self.subtitle
        published.parent = self.parent
        published.problem_count = self.problem_count
        published.description = self.description
        published.publish_date = self.publish_date
        published.url = self.url
        published.save()
        # Find DraftProblem which depend upon this and convert their `draft_source` to `source`
        dependents = DraftProblem.objects.filter(draft_source=self)

        for dep in dependents:
            dep.draft_source = None
            dep.source = published
            dep.save()

        return published


class DraftProblem(Draftable, models.Model):
    problem_text = models.TextField(blank=True, null=True)
    has_answer = models.BooleanField(default=False)
    answer_text = models.TextField(blank=True, null=True)

    source = models.ForeignKey(Source, on_delete=models.SET_NULL, null=True, blank=True)
    draft_source = models.ForeignKey(
        DraftSource, on_delete=models.SET_NULL, null=True, blank=True
    )
    number = models.PositiveSmallIntegerField(null=True, blank=True)

    @classmethod
    def create_from_published(cls, published):
        obj = cls.objects.create()
        obj.problem_text = published.problem_text
        obj.has_answer = published.has_answer
        obj.answer_text = published.answer_text
        obj.source = published.source
        obj.number = published.number
        return obj

    def convert_to_published(self, existing=None):
        if existing is None:
            published = Problem()
        else:
            published = existing
        published.problem_text = self.problem_text
        published.has_answer = self.has_answer
        published.answer_text = self.answer_text
        if self.draft_source is not None:
            raise DraftDependsOnOtherDraft("Problem draft depends on a draft source")
        published.source = self.source
        published.number = self.number

        dependents = DraftSolution.objects.filter(draft_problem=self)

        for dep in dependents:
            dep.draft_problem = None
            dep.draft_problem = published
            dep.save()

        return published


class DraftSolution(Draftable, models.Model):
    problem = models.ForeignKey(
        Problem, on_delete=models.SET_NULL, blank=True, null=True
    )
    draft_problem = models.ForeignKey(
        DraftProblem, on_delete=models.SET_NULL, blank=True, null=True
    )
    solution_text = models.TextField()

    @classmethod
    def create_from_published(cls, published):
        obj = cls.objects.create()
        obj.problem = published.problem
        obj.solution_text = published.solution_text
        return obj

    def convert_to_published(self, existing=None):
        if existing is None:
            published = SourceGroup()
        else:
            published = existing

        published.solution_text = self.solution_text
        if self.draft_problem is not None:
            raise DraftDependsOnOtherDraft("Solution draft depends on a draft problem")
        published.problem = self.problem
        published.save()

        return published


class DraftPublishError(Exception):
    def __init__(self, message):
        super().__init__(message)


class DraftDependsOnOtherDraft(DraftPublishError):
    def __init__(self, message):
        super().__init__(message)
