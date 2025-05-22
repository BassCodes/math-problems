import pytest
from accounts.models import CustomUser
from django.core.exceptions import ValidationError


@pytest.mark.django_db
def test_username_too_long():
    user = CustomUser.objects.create(
        password="test", username="long_but_otherwise_valid_username"
    )
    with pytest.raises(ValidationError):
        user.full_clean()


@pytest.mark.django_db
def test_username_with_uppercase():
    user = CustomUser.objects.create(password="test", username="VERY_LOUD_USERNAME")
    with pytest.raises(ValidationError):
        user.full_clean()


@pytest.mark.django_db
def test_username_with_special_characters():
    user = CustomUser.objects.create(password="test", username="fun$@!^#")
    with pytest.raises(ValidationError):
        user.full_clean()


@pytest.mark.django_db
def test_valid_username_all_lowercase():
    user = CustomUser.objects.create(password="test", username="alexander")
    user.full_clean()


@pytest.mark.django_db
def test_valid_username_with_underscore():
    user = CustomUser.objects.create(password="test", username="bob_dylan")
    user.full_clean()


@pytest.mark.django_db
def test_valid_username_with_numbers():
    user = CustomUser.objects.create(password="test", username="173489")
    user.full_clean()


@pytest.mark.django_db
def test_valid_username_with_all_allowable_features():
    user = CustomUser.objects.create(password="test", username="0hello_there_1984_")
    user.full_clean()
