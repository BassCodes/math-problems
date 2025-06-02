from django.contrib.auth import get_user_model
import pytest

from editor.models import (
    DraftSource,
    DraftSourceGroup,
    DraftProblem,
    DraftSolution,
    DraftRef,
)
from problems.models import Problem, Source
from editor.exceptions import DraftDependsOnOtherDraft, AttemptToDoubleForkObject
from django.db.utils import IntegrityError
from django.core.exceptions import ValidationError
from django.db import transaction


@pytest.mark.django_db
def test_create_source_draft_from_existing():
    user = get_user_model().objects.create(username="Foo", password="Bar")
    gold_source = Source.objects.create(name="FoobarSource")

    draft = DraftSource.create_new(user, gold_source)

    assert draft.name == gold_source.name

    assert draft.get_forked_object() == gold_source
    assert draft.is_fork()


@pytest.mark.django_db
def test_source_draft_merge_back_into_fork():
    user = get_user_model().objects.create(username="Foo", password="Bar")
    gold_source = Source.objects.create(name="FoobarSource")
    gold_pk = gold_source.pk

    draft = DraftSource.create_new(user, gold_source)
    assert draft.get_forked_object() == gold_source
    assert draft.is_fork()

    assert draft.name == gold_source.name
    draft.name = "FroobazSource"
    assert draft.name != gold_source.name

    draft.send_to_review()
    published = draft.publish()
    assert published.pk == gold_pk
    assert published.name == "FroobazSource"


@pytest.mark.django_db
def test_problem_draft_publish_with_source_dependency():
    user = get_user_model().objects.create(username="Foo", password="Bar")
    source_draft = DraftSource.create_new(user, name="Foo Draft", slug="foo")
    assert source_draft.slug == "foo"
    problem_draft = DraftProblem.create_new(user, problem_text="Bar problem", number=1)
    assert not problem_draft.is_fork()
    assert not source_draft.is_fork()
    source_draft.save()
    problem_draft.draft_source = source_draft
    problem_draft.save()
    problem_draft.send_to_review()

    with pytest.raises(DraftDependsOnOtherDraft) as e_info:
        problem_draft.publish()

    source_draft.send_to_review()
    assert problem_draft.draft_source == source_draft
    source_published = source_draft.publish()
    assert source_published.slug == "foo"
    problem_draft.refresh_from_db()
    assert problem_draft.source == source_published
    assert problem_draft.draft_source is None
    problem_published = problem_draft.publish()
    assert problem_published.source.name == "Foo Draft" == source_published.name
    assert Problem.objects.exists()
    assert Source.objects.exists()


@pytest.mark.django_db
def test_publish_draft_with_draft_dependencies():
    user = get_user_model().objects.create(username="Foo", password="Bar")
    draft_source = DraftSource.create_new(user, name="test source")

    draft_prob = DraftProblem.create_new(user, problem_text="test problem text foo bar")
    draft_prob.draft_source = draft_source

    draft_prob.send_to_review()
    with pytest.raises(DraftDependsOnOtherDraft) as e_info:
        draft_prob.publish()


@pytest.mark.django_db
def test_source_draft_publishing_flow():
    user = get_user_model().objects.create(username="Foo", password="Bar")

    draft = DraftSource.create_new(user, name="Baz", slug="baz")
    assert not draft.is_fork()
    assert draft.name == "Baz"
    ref = draft.draft_ref
    draft_pk = draft.pk
    ref_pk = ref.pk

    draft_ref = draft.draft_ref
    assert draft_ref == ref

    # Can only publish when in review
    with pytest.raises(AssertionError) as e_info:
        draft.publish()

    draft.send_to_review()
    assert draft.draft_ref.draft_state == DraftRef.DraftState.IN_REVIEW

    # Draft can't be put into review when already in review
    with pytest.raises(AssertionError) as e_info:
        draft.send_to_review()

    # Publish draft
    published = draft.publish()
    assert published is not None
    # Check if draft has been deleted
    assert not DraftSource.objects.filter(pk=draft_pk).exists()
    assert not DraftRef.objects.filter(pk=ref_pk).exists()

    # Ensure published exists
    assert Source.objects.filter(name="Baz").exists()


@pytest.mark.django_db
def test_draft_deletion_deletes_ref():
    user = get_user_model().objects.create(username="Foo", password="Bar")
    draft = DraftSource.create_new(user, name="FoobarSource")
    ref_pk = draft.draft_ref.pk

    draft.delete()
    assert not DraftRef.objects.filter(pk=ref_pk).exists()


@pytest.mark.django_db
def test_draft_dependency_finding():
    user = get_user_model().objects.create(username="Foo", password="Bar")
    draft_src_group = DraftSourceGroup.create_new(user, name="FroobarGroup")
    draft_src = DraftSource.create_new(user, name="FoobarSource")

    assert not draft_src.has_draft_dependencies()
    draft_src.draft_parent = draft_src_group
    assert draft_src.has_draft_dependencies()

    [dep] = draft_src.get_draft_dependencies()

    assert dep == draft_src_group

    [dep2] = draft_src.chase_draft_dependencies()
    assert dep2 == dep

    draft_problem = DraftProblem.create_new(user, problem_text="Foo bar baz")
    draft_problem.draft_source = draft_src

    assert draft_problem.has_draft_dependencies()

    [dep3] = draft_problem.get_draft_dependencies()
    assert dep3 == draft_src

    [dep4, dep5] = draft_problem.chase_draft_dependencies()

    assert dep4 == draft_src
    assert dep5 == draft_src_group

    draft_src_group.delete()
    draft_src.refresh_from_db()
    assert not draft_src.has_draft_dependencies()

    draft_src.delete()
    draft_problem.refresh_from_db()
    assert not draft_problem.has_draft_dependencies()


@pytest.mark.django_db
def test_draft_not_mutated_in_failed_attempt_to_publish():
    user = get_user_model().objects.create(username="Foo", password="Bar")
    # Source can't be published because it doesn't have a slug
    draft_src = DraftSource.create_new(user, name="FoobarSource")
    draft_problem = DraftProblem.create_new(user, problem_text="Baz?")
    draft_problem.draft_source = draft_src
    draft_problem.save()

    assert draft_src.draft_ref.draft_state == DraftRef.DraftState.DRAFT

    draft_src.send_to_review()

    # Source https://stackoverflow.com/a/23326971
    with transaction.atomic():
        with pytest.raises(IntegrityError) as e_info:
            draft_src.publish()

    draft_src.refresh_from_db()
    draft_problem.refresh_from_db()

    # ensure source draft state not mutated
    assert draft_src.draft_ref.draft_state == DraftRef.DraftState.IN_REVIEW

    # ensure problem draft state not mutated
    assert draft_problem.source is None
    assert draft_problem.draft_source == draft_src


@pytest.mark.django_db
def test_draft_publish_errors():
    src = Source(name="baba")
    # Ensure source requires slug to be NOT NULL
    with pytest.raises(ValidationError) as e_info:
        src.clean_fields()

    user = get_user_model().objects.create(username="Foo", password="Bar")
    draft_src = DraftSource.create_new(user, name="foo")

    [e] = draft_src.get_publish_errors()
    assert e.__class__ is ValidationError
    # Ensure that `get_publish_errors` does not create any published objects
    assert not Source.objects.all().exists()

    draft_source_group = DraftSourceGroup.create_new(user, name="baz")
    draft_src.draft_parent = draft_source_group
    draft_src.save()

    [e1, e2] = draft_src.get_publish_errors()
    assert e1.__class__ is ValidationError, e2.__class__ is DraftDependsOnOtherDraft

    draft_source_group.delete()

    draft_src.refresh_from_db()
    draft_src.slug = "bar"
    draft_src.save()
    assert draft_src.get_publish_errors() == []


@pytest.mark.django_db
def test_draft_publish_errors_does_not_create_published_objects():
    """
    `get_publish_errors` must create an instance of the published object to
    verify it has no errors. Ensure that the published instance is not saved to
    the database.
    """
    user = get_user_model().objects.create(username="Foo", password="Bar")
    draft_src = DraftSource.create_new(user, name="foo", slug="bar")

    assert draft_src.get_publish_errors() == []

    assert not Source.objects.all().exists()


@pytest.mark.django_db
def test_draft_can_only_be_forked_once_per_user():
    user = get_user_model().objects.create(username="Foo", password="Bar")
    source = Source.objects.create(name="test", slug="foo")

    draft_src = DraftSource.create_new(user, forked_from=source)
    with pytest.raises(AttemptToDoubleForkObject) as e_info:
        DraftSource.create_new(user, forked_from=source)
