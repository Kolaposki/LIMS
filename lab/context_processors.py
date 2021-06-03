from users.models import *


def user_details_processor(request):
    details = UserProfile.objects.get(user=request.user)
    print("details: ", details)

    if not details:
        print("No user_details")
        return {'user_details': None}

    return {'user_details': details}
