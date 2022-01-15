import pytest


@pytest.fixture
def create_user(db, django_user_model):
    def make_user(**kwargs):
        return django_user_model.objects.create_user(**kwargs)

    return make_user


@pytest.fixture
def create_superuser(db, django_user_model):
    def make_user(**kwargs):
        return django_user_model.objects.create_superuser(**kwargs)

    return make_user


@pytest.mark.django_db
def test_create_user(create_user):
    user = create_user(email="normal@user.com", password="foo")

    assert user.email == "normal@user.com"
    assert user.is_active
    assert not user.is_staff
    assert not user.is_superuser


@pytest.mark.django_db
@pytest.mark.parametrize(
    "email, password",
    [
        (None, None),
        ("normal@user.com", None),
        ("", "foo"),
    ],
)
def test_negative_create_user(email, password, create_user):
    with pytest.raises(ValueError):
        create_user(email=email, password=password)


@pytest.mark.django_db
def test_not_exist_username(create_user):
    user = create_user(email="normal@user.com", password="foo")

    assert user.username is None


@pytest.mark.django_db
def test_create_superuser(create_superuser):
    admin_user = create_superuser(email="super@user.com", password="foo")

    assert admin_user.email == "super@user.com"
    assert admin_user.is_active
    assert admin_user.is_staff
    assert admin_user.is_superuser


@pytest.mark.django_db
def test_negative_create_superuser(create_superuser):

    with pytest.raises(ValueError):
        create_superuser(email="super@user.com", password="foo", is_superuser=False)


@pytest.mark.django_db
def test_not_exist_admin_username(create_superuser):
    admin_user = create_superuser(
        email="super@user.com",
        password="foo",
    )

    assert admin_user.username is None
