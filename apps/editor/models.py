from django.db import models
from django.urls import reverse
from simple_history.models import HistoricalRecords

from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType

from problems.models import Source, SourceGroup, Problem, Solution
from accounts.models import CustomUser


from .exceptions import DraftDependsOnOtherDraft


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

    forked_object_id = models.PositiveIntegerField(null=True)
    forked_content_type = models.ForeignKey(
        ContentType, on_delete=models.CASCADE, related_name="+", null=True
    )
    forked_content_object = GenericForeignKey("forked_content_type", "forked_object_id")

    @classmethod
    def _create_new(cls, user, forked_from=None):
        new_draft_ref = cls(draft_owner=user)
        if forked_from is not None:
            forked_ctype = ContentType.objects.get_for_model(forked_from.__class__)
            new_draft_ref.forked_content_type = forked_ctype
            new_draft_ref.forked_content_object = forked_from
        return new_draft_ref


class DraftManager(models.Manager):
    def query_set(self):
        return DraftQuerySet(self.model)


class DraftQuerySet(models.query.QuerySet):
    def owned_by(self, owner):
        return self.filter(draft_ref__draft_owner=owner)


class DraftableMixin(models.Model):
    class Meta:
        abstract = True

    class DraftMeta:
        reference_model = None
        copy_fields = []
        draftable_foreign_keys = {}
        dependents = []

    draft_ref = models.OneToOneField(DraftRef, on_delete=models.CASCADE)

    objects = DraftManager()

    @classmethod
    def create_new(cls, user, forked_from=None, **kwargs):
        if forked_from is not None:
            obj = cls.__create_from_published(forked_from)
        else:
            obj = cls(**kwargs)
        draft_ref = DraftRef._create_new(user, forked_from=forked_from)
        draft_ref.save()
        obj.draft_ref = draft_ref
        obj.save()
        return obj

    @classmethod
    def __create_from_published(cls, published):
        obj = cls()
        obj.__copy_fields_from_object(published)
        return obj

    def __copy_fields_from_object(self, obj):
        for field in self.DraftMeta.copy_fields:
            setattr(self, field, getattr(obj, field))

    def __verify_foreign_keys_are_not_drafts(self):
        for fk, draft_fk in self.DraftMeta.draftable_foreign_keys.items():
            if getattr(self, draft_fk) is not None:
                raise DraftDependsOnOtherDraft(
                    f"Foreign Key `{draft_fk}` is still in draft state. (unpublished)"
                )

    def __copy_fields_to_object(self, obj):
        for field in self.DraftMeta.copy_fields:
            setattr(obj, field, getattr(self, field))

    def __update_dependents_post_publish(self, published):
        for [cls, draft_name, pub_name] in self.DraftMeta.dependents:
            f = draft_name
            dependents = cls.objects.filter(**{f: self})
            for dep in dependents:
                setattr(dep, draft_name, None)
                setattr(dep, pub_name, published)
                dep.save()

    def __convert_to_published(self, forked_from=None):
        assert self.DraftMeta.reference_model is not None
        self.__verify_foreign_keys_are_not_drafts()

        if forked_from is None:
            published = self.DraftMeta.reference_model()
        else:
            # TODO handle history
            published = forked_from

        self.__copy_fields_to_object(published)
        published.save()
        self.__update_dependents_post_publish(published)

        return published

    def publish(self):
        ref = self.draft_ref
        assert ref.draft_state == DraftRef.DraftState.IN_REVIEW

        published = self.__convert_to_published(ref.forked_content_object)
        self.draft_ref.delete()
        self.delete()
        return published

    def send_to_review(self):
        ref = self.draft_ref
        assert ref.draft_state == DraftRef.DraftState.DRAFT
        ref.draft_state = DraftRef.DraftState.IN_REVIEW
        ref.save()

    def fail_review_to_draft(self):
        ref = self.draft_ref
        assert ref.draft_state == DraftRef.DraftState.IN_REVIEW
        ref.draft_state = DraftRef.DraftState.DRAFT
        ref.save()

    def get_forked_object(self):
        forked = self.draft_ref.forked_content_object
        if forked is not None:
            assert forked.__class__ == self.DraftMeta.reference_model
        return forked

    def is_fork(self):
        return self.get_forked_object() is not None


class DraftSolution(DraftableMixin, models.Model):
    problem = models.ForeignKey(
        Problem, on_delete=models.SET_NULL, blank=True, null=True
    )
    draft_problem = models.ForeignKey(
        "DraftProblem", on_delete=models.SET_NULL, blank=True, null=True
    )
    solution_text = models.TextField()

    class DraftMeta(DraftableMixin.DraftMeta):
        reference_model = Solution
        copy_fields = ["problem", "solution_text"]
        draftable_foreign_keys = {"problem": "draft_problem"}


class DraftProblem(DraftableMixin, models.Model):
    problem_text = models.TextField(blank=True, null=True)
    has_answer = models.BooleanField(default=False)
    answer_text = models.TextField(blank=True, null=True)

    source = models.ForeignKey(Source, on_delete=models.SET_NULL, null=True, blank=True)
    draft_source = models.ForeignKey(
        "DraftSource", on_delete=models.SET_NULL, null=True, blank=True
    )
    number = models.PositiveSmallIntegerField(null=True, blank=True)

    class DraftMeta(DraftableMixin.DraftMeta):
        reference_model = Problem
        copy_fields = ["problem_text", "has_answer", "answer_text", "source", "number"]
        draftable_foreign_keys = {"source": "draft_source"}
        dependents = [(DraftSolution, "draft_problem", "problem")]


class DraftSource(DraftableMixin, models.Model):
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
        "DraftSourceGroup",
        on_delete=models.SET_NULL,
        blank=True,
        null=True,
    )
    problem_count = models.PositiveSmallIntegerField(blank=True, null=True)
    description = models.TextField(blank=True, null=True)
    publish_date = models.DateField(blank=True, null=True)
    url = models.URLField(blank=True, null=True)

    class DraftMeta(DraftableMixin.DraftMeta):
        reference_model = Source
        copy_fields = [
            "slug",
            "name",
            "shortname",
            "subtitle",
            "parent",
            "problem_count",
        ]
        draftable_foreign_keys = {"parent": "draft_parent"}
        dependents = [(DraftProblem, "draft_source", "source")]


class DraftSourceGroup(DraftableMixin, models.Model):
    name = models.CharField(max_length=128, blank=True, null=True)
    description = models.TextField(blank=True, null=True)
    url = models.URLField(blank=True, null=True)

    class DraftMeta(DraftableMixin.DraftMeta):
        reference_model = SourceGroup
        copy_fields = ["name", "description", "url"]
        dependents = [(DraftSource, "draft_parent", "parent")]
