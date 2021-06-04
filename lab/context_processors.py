from users.models import *


def user_details_processor(request):
    if request.user.is_anonymous:
        print("No user_details ANONYMOUSUSER")
        return {'user_details': None}

    try:
        details = UserProfile.objects.get(user=request.user)
    except UserProfile.DoesNotExist:
        print("No user_details")
        return {'user_details': None}

    print("details: ", details)

    return {'user_details': details}
