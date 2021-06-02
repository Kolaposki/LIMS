from django import template
from users.models import UserProfile

register = template.Library()


@register.filter
def remove_url(url):
    """Returns the url base"""
    return url.split("/")[1]


@register.filter
def check_permission(user):
    """check_permission"""
    logged_user_profile = UserProfile.objects.get(user=user)
    # print("check_permission: logged_user_profile officer: ", logged_user_profile.is_officer)
    # print("check_permission: logged_user_profile senator: ", logged_user_profile.is_senator)

    if logged_user_profile:
        if logged_user_profile.is_officer is True:
            return 'officer'
        else:
            return 'senator'

    return ''
