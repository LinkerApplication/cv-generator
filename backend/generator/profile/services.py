from .models import Profile


def check_user_has_profile(user):
    """
    if user already has profile return True, else False
    """
    has_profile = hasattr(user, "profile")

    return bool(user and user.is_authenticated and has_profile)


def get_user_profile(pk: int):
    """
    if user has profile return model Profile, else False
    """
    try:
        return Profile.objects.get(pk=pk)
    except Exception:
        return False
