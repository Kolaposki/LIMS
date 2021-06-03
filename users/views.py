from django.shortcuts import render, redirect
from django_registration.backends.one_step.views import RegistrationView
from django.urls import reverse_lazy
from django.contrib import messages
from .forms import UserRegistrationForm

from .forms import *
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse, JsonResponse, HttpResponseBadRequest
from django.shortcuts import render, redirect, get_object_or_404
from django.template.loader import render_to_string
from django.conf import settings

from django.views.decorators.csrf import csrf_exempt

# email service start #
from django.shortcuts import render, redirect
from django.core.mail import send_mail, BadHeaderError
from django.http import HttpResponse
from django.contrib.auth.forms import PasswordResetForm
from django.contrib.auth.models import User
from django.template.loader import render_to_string
from django.db.models.query_utils import Q
from django.utils.http import urlsafe_base64_encode
from django.contrib.auth.tokens import default_token_generator
from django.utils.encoding import force_bytes
from django.contrib.auth import logout
from django_hosts.resolvers import reverse as host_reverse
from django.core import mail
from django.utils.html import strip_tags

from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect
from django.core.mail import EmailMultiAlternatives
from django import template
from django.core.mail import EmailMessage


def logout_user(request):
    print("logging out ", request.user)
    logout(request)
    return redirect(to='login', permanent=True)


# Registration View
class UserRegistrationView(RegistrationView):
    template_name = "register.html"
    success_url = settings.LOGIN_REDIRECT_URL
    form_class = UserRegistrationForm


@login_required
def profile(request):
    user_obj = User.objects.filter(pk=request.user.pk)
    my_email = request.user.email
    update_profile_form = ProfileUpdateForm(instance=request.user.userprofile)

    context = {
        'update_profile_form': update_profile_form,
        'my_email': my_email,
    }
    return render(request, 'users/profile.html', context=context)


# Updating of profile using ajax
@login_required
@csrf_exempt
def update_profile(request):
    if request.is_ajax() and request.method == 'POST':

        user_update_form = UserUpdateForm(request.POST, instance=request.user)
        update_profile_form = ProfileUpdateForm(request.POST, request.FILES, instance=request.user.userprofile)

        if user_update_form.is_valid() and update_profile_form.is_valid():
            update_profile_form.save()
            user_update_form.save()

            logged_user_profile = UserProfile.objects.get(user=request.user.pk)
            cover_img = str(logged_user_profile.cover_img.url)
            username = logged_user_profile.user.username
            description = logged_user_profile.description
            full_name = logged_user_profile.full_name

            data_dict = {'error': False,
                         "message": "Profile updated successfully",
                         "cover_img": cover_img, "full_name": full_name, "description": description,
                         "username": username}

            return JsonResponse(data=data_dict)
        else:
            form_err = ''
            if user_update_form.errors:
                form_err = user_update_form.errors
                print("user_update_form error")
            elif update_profile_form.errors:
                form_err = update_profile_form.errors
                print("update_profile_form error")

            print(form_err)

            return JsonResponse(
                {'error': True, 'message': 'An error occurred while updating profile. Please check the form',
                 "form_err": form_err})
    else:
        return JsonResponse({'error': True, 'message': 'Unrecognized request'})
