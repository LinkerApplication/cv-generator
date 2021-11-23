def user_can_create_profile(request):
    """
    if user already has profile return False, else True
    """
    has_profile = hasattr(request.user, 'profile')

    return bool(request.user and request.user.is_authenticated and not has_profile)


def user_can_create_experience(request):
    """
    if user has profile return True, else False
    """
    has_profile = hasattr(request.user, 'profile')

    return bool(request.user and request.user.is_authenticated and has_profile)
