from django.contrib.auth import get_user_model
import pytest

from editor.models import DraftSource, DraftProblem, DraftRef, DraftDependsOnOtherDraft
from problems.models import Problem, Source


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
    ref = draft.get_draft_ref()
    draft_pk = draft.pk
    ref_pk = ref.pk

    draft_ref = draft.get_draft_ref()
    assert draft_ref == ref

    # Can only publish when in review
    with pytest.raises(AssertionError) as e_info:
        draft.publish()

    draft.send_to_review()
    assert draft.get_draft_ref().draft_state == DraftRef.DraftState.IN_REVIEW

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
