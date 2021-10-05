import pytest
from django.contrib.auth import get_user_model


@pytest.mark.django_db
def test_create_user():
    User = get_user_model()
    user = User.objects.create_user(email='normal@user.com', password='foo')
    assert user.email == 'normal@user.com'
    assert user.is_active
    assert not user.is_staff
    assert not user.is_superuser


@pytest.mark.django_db
def test_negative_create_user():
    User = get_user_model()
    with pytest.raises(TypeError):
        user = User.objects.create_user()
        if user.email is None or user.password is None:
            raise TypeError
    with pytest.raises(TypeError):
        user = User.objects.create_user(email='')
        if user.password is None:
            raise TypeError
    with pytest.raises(ValueError):
        user = User.objects.create_user(email='', password="foo")


@pytest.mark.django_db
def test_not_exist_username():
    User = get_user_model()
    user = User.objects.create_user(email='normal@user.com', password='foo')

    try:
        # username is None for the AbstractUser option
        # username does not exist for the AbstractBaseUser option
        assert user.username is None
    except AttributeError:
        pass


@pytest.mark.django_db
def test_create_superuser():
    User = get_user_model()
    admin_user = User.objects.create_superuser(email='super@user.com', password='foo')
    assert admin_user.email == 'super@user.com'
    assert admin_user.is_active
    assert admin_user.is_staff
    assert admin_user.is_superuser


@pytest.mark.django_db
def test_negative_create_superuser():
    User = get_user_model()

    with pytest.raises(ValueError):
        User.objects.create_superuser(
            email='super@user.com', password='foo', is_superuser=False
        )


@pytest.mark.django_db
def test_not_exist_admin_username():
    User = get_user_model()
    admin_user = User.objects.create_superuser(email='super@user.com', password='foo')

    try:
        # username is None for the AbstractUser option
        # username does not exist for the AbstractBaseUser option
        assert admin_user.username is None
    except AttributeError:
        pass
