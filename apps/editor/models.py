from django.db import models
from django.db.models import Q

from django.urls import reverse
from simple_history.models import HistoricalRecords

from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType

from problems.models import Source, SourceGroup, Problem, Solution
from accounts.models import CustomUser

from .exceptions import DraftDependsOnOtherDraft, AttemptToDoubleForkObject
from django.core.exceptions import ValidationError, ObjectDoesNotExist

from history.models import HistoryPublishDataShim


from utility import PascalCaseToSnakeCase


class DraftQuerySet(models.query.QuerySet):
    def owned_by(self, owner):
        return self.filter(draft_ref__draft_owner=owner)


class DraftRefQuerySet(models.query.QuerySet):
    def by_owner(self, user):
        return self.filter(draft_owner=user)

    def by_forked(self, forked_object):
        return self.filter(
            forked_object_id=forked_object.id,
            forked_content_type=ContentType.objects.get_for_model(forked_object),
        )


class DraftRef(models.Model):
    """
    Holds metadata about a draft.
    """

    class DraftState(models.TextChoices):
        DRAFT = ("DR", "Draft")
        IN_REVIEW = ("RE", "In Review")

    draft_owner = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    draft_created = models.DateTimeField(auto_now=True)
    draft_edited = models.DateTimeField(auto_now_add=True)
    draft_state = models.CharField(max_length=2, choices=DraftState, default=DraftState.DRAFT)

    forked_object_id = models.PositiveIntegerField(null=True)
    forked_content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE, related_name="+", null=True)
    forked_content_object = GenericForeignKey("forked_content_type", "forked_object_id")

    objects = DraftRefQuerySet.as_manager()

    @classmethod
    def create_new(cls, user, forked_from=None):
        print(DraftableMixin.__subclasses__())
        new_draft_ref = cls(draft_owner=user)
        if forked_from is not None:
            forked_ctype = ContentType.objects.get_for_model(forked_from.__class__)
            new_draft_ref.forked_content_type = forked_ctype
            new_draft_ref.forked_content_object = forked_from
        return new_draft_ref

    def get_draft(self):
        for draft_class in DraftableMixin.__subclasses__():
            try:
                return draft_class.objects.get(draft_ref=self)
            except ObjectDoesNotExist:
                continue
        raise ObjectDoesNotExist()


class DraftableMixin(models.Model):
    class Meta:
        abstract = True

    class DraftMeta:
        reference_model = None
        copy_fields = []
        draftable_foreign_keys = {}
        dependents = []

    draft_ref = models.OneToOneField(DraftRef, on_delete=models.CASCADE)

    objects = DraftQuerySet().as_manager()

    @classmethod
    def create_new(cls, user, forked_from=None, **kwargs):
        if forked_from is not None:
            if DraftRef.objects.by_owner(user).by_forked(forked_from).exists():
                raise AttemptToDoubleForkObject("TODO")

            obj = cls.__create_from_published(forked_from)
        else:
            obj = cls(**kwargs)
        draft_ref = DraftRef.create_new(user, forked_from=forked_from)
        draft_ref.save()
        obj.draft_ref = draft_ref
        obj.save()
        return obj

    def delete(self, *args, **kwargs):
        self.__update_dependents_post_delete()
        self.draft_ref.delete()
        super().delete(*args, **kwargs)

    @classmethod
    def __create_from_published(cls, published):
        obj = cls()
        obj.__copy_fields_from_object(published)
        return obj

    def has_draft_dependencies(self):
        return self.get_draft_dependencies() != []

    def get_draft_dependencies(self):
        dep = []
        for fk, draft_fk in self.DraftMeta.draftable_foreign_keys.items():
            rel = getattr(self, draft_fk)
            if rel is not None:
                dep.append(rel)

        return dep

    def chase_draft_dependencies(self):
        # If there is more than one result to `get_draft_dependencies`
        # then this function should be converted to breadth first search
        deps = []
        for dep in self.get_draft_dependencies():
            deps.append(dep)
            for d in dep.chase_draft_dependencies():
                deps.append(d)

        return deps

    def __copy_fields_from_object(self, obj):
        for field in self.DraftMeta.copy_fields:
            setattr(self, field, getattr(obj, field))

    def __copy_fields_to_object(self, obj):
        for field in self.DraftMeta.copy_fields:
            setattr(obj, field, getattr(self, field))

    def __verify_foreign_keys_are_not_drafts(self):
        for fk, draft_fk in self.DraftMeta.draftable_foreign_keys.items():
            if getattr(self, draft_fk) is not None:
                raise DraftDependsOnOtherDraft(f"Foreign Key `{draft_fk}` is still in draft state. (unpublished)")

    # TODO: Combine with other update dependents method?
    def __update_dependents_post_publish(self, published):
        for [cls, draft_name, pub_name] in self.DraftMeta.dependents:
            f = draft_name
            dependents = cls.objects.filter(**{f: self})
            for dep in dependents:
                setattr(dep, draft_name, None)
                setattr(dep, pub_name, published)
                dep.save()

    def __update_dependents_post_delete(self):
        for [cls, draft_name, pub_name] in self.DraftMeta.dependents:
            f = draft_name
            dependents = cls.objects.filter(**{f: self})
            for dep in dependents:
                setattr(dep, draft_name, None)
                dep.save()

    def get_publish_errors(self):
        """
        Capture all exceptions that would inhibit publishing draft object.
        Returns as a list of exceptions, or empty list
        """
        published = self.__get_published_object()
        exceptions = []
        try:
            published.clean_fields()
        except ValidationError as e:
            exceptions.append(e)
        try:
            self.__verify_foreign_keys_are_not_drafts()
        except DraftDependsOnOtherDraft as e:
            exceptions.append(e)
        return exceptions

    def __get_published_object(self):
        assert self.DraftMeta.reference_model is not None
        if self.draft_ref.forked_content_object is None:
            published = self.DraftMeta.reference_model()
        else:
            published = self.draft_ref.forked_content_object
        self.__copy_fields_to_object(published)
        return published

    def __convert_to_published(self):
        self.__verify_foreign_keys_are_not_drafts()
        published = self.__get_published_object()
        published.save()
        self.__update_dependents_post_publish(published)

        return published

    def publish(self, publishing_user):
        ref = self.draft_ref
        assert ref.draft_state == DraftRef.DraftState.IN_REVIEW
        if publishing_user is None:
            raise ObjectDoesNotExist("todo")

        published = self.__convert_to_published()
        h = published.history.first()
        h.history_publish_type = HistoryPublishDataShim.PublishType.MERGED
        h.history_publish_reviewer = publishing_user
        h.history_publish_author = ref.draft_owner
        h.save()
        self.delete()
        return published

    def force_publish(self, publishing_user):
        if publishing_user is None:
            raise ObjectDoesNotExist("todo")
        ref = self.draft_ref
        if ref.draft_state == DraftRef.DraftState.DRAFT:
            self.send_to_review()

        published = self.__convert_to_published()
        h = published.history.first()
        h.history_publish_type = HistoryPublishDataShim.PublishType.FORCE_PUBLISHED
        h.history_publish_reviewer = publishing_user
        h.history_publish_author = ref.draft_owner
        h.save()
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

    def is_draft(self):
        """
        Returns true always. To be used in situations when both a published and
        draft object are to be used interchangeably.
        """
        return True

    def is_user_deletable(self):
        return self.draft_ref.draft_state == DraftRef.DraftState.DRAFT

    def __str__(self):
        # To be overloaded
        return self.model_name_and_id_str()

    def model_name_and_id_str(self):
        return f"Draft {self.DraftMeta.reference_model.__name__} ID#{self.pk}"

    def get_absolute_url(self):
        url_name = f"draft_{PascalCaseToSnakeCase.convert(self.DraftMeta.reference_model.__name__)}"
        return reverse(url_name, kwargs={"pk": self.pk})

    def get_absolute_edit_url(self):
        url_name = f"draft_{PascalCaseToSnakeCase.convert(self.DraftMeta.reference_model.__name__)}_edit"
        return reverse(url_name, kwargs={"pk": self.pk})

    def get_absolute_delete_url(self):
        url_name = f"draft_{PascalCaseToSnakeCase.convert(self.DraftMeta.reference_model.__name__)}_delete"
        return reverse(url_name, kwargs={"pk": self.pk})

    def get_absolute_force_publish_url(self):
        url_name = f"draft_{PascalCaseToSnakeCase.convert(self.DraftMeta.reference_model.__name__)}_force_publish"
        return reverse(url_name, kwargs={"pk": self.pk})

    def get_absolute_forked_from_url(self):
        if self.draft_ref.forked_content_object:
            return self.draft_ref.forked_content_object.get_absolute_url()
        else:
            return None


#
# Draft Models
#


class DraftSolution(DraftableMixin, models.Model):
    problem = models.ForeignKey(Problem, on_delete=models.SET_NULL, blank=True, null=True)
    draft_problem = models.ForeignKey("DraftProblem", on_delete=models.SET_NULL, blank=True, null=True)
    solution_text = models.TextField()

    class DraftMeta(DraftableMixin.DraftMeta):
        reference_model = Solution
        copy_fields = ["problem", "solution_text"]
        draftable_foreign_keys = {"problem": "draft_problem"}

    class Meta:
        constraints = [
            models.CheckConstraint(
                condition=~(Q(problem__isnull=False) & Q(draft_problem__isnull=False)),
                name="draft_solution_no_problem_duplication",
            )
        ]


class DraftProblem(DraftableMixin, models.Model):
    problem_text = models.TextField(blank=True, null=True)
    has_answer = models.BooleanField(default=False)
    answer_text = models.TextField(blank=True, null=True)

    source = models.ForeignKey(Source, on_delete=models.SET_NULL, null=True, blank=True)
    draft_source = models.ForeignKey("DraftSource", on_delete=models.SET_NULL, null=True, blank=True)
    number = models.PositiveSmallIntegerField(null=True, blank=True)

    class DraftMeta(DraftableMixin.DraftMeta):
        reference_model = Problem
        copy_fields = ["problem_text", "has_answer", "answer_text", "source", "number"]
        draftable_foreign_keys = {"source": "draft_source"}
        dependents = [(DraftSolution, "draft_problem", "problem")]

    class Meta:
        constraints = [
            models.CheckConstraint(
                condition=~(Q(source__isnull=False) & Q(draft_source__isnull=False)),
                name="draft_problem_no_source_duplication",
            )
        ]


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
            "description",
            "publish_date",
            "url",
        ]
        draftable_foreign_keys = {"parent": "draft_parent"}
        dependents = [(DraftProblem, "draft_source", "source")]

    class Meta:
        constraints = [
            models.CheckConstraint(
                condition=~(Q(parent__isnull=False) & Q(draft_parent__isnull=False)),
                name="draft_source_no_parent_duplication",
            )
        ]


class DraftSourceGroup(DraftableMixin, models.Model):
    name = models.CharField(max_length=128, blank=True, null=True)
    description = models.TextField(blank=True, null=True)
    url = models.URLField(blank=True, null=True)

    class DraftMeta(DraftableMixin.DraftMeta):
        reference_model = SourceGroup
        copy_fields = ["name", "description", "url"]
        dependents = [(DraftSource, "draft_parent", "parent")]

    def __str__(self):
        return self.name
