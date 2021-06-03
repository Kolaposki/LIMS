from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django_registration.forms import RegistrationFormUniqueEmail
from .models import UserProfile


class UserRegistrationForm(RegistrationFormUniqueEmail):
    class Meta(RegistrationFormUniqueEmail.Meta):
        model = User
        fields = ["username", "email", "password1", "password2"]


class ProfileUpdateForm(forms.ModelForm):
    class Meta:
        model = UserProfile
        fields = ['first_name', 'last_name', 'other_name',]
        # faculty = forms.ChoiceField(widget=forms.Select(attrs={'class': 'form-control', }))
        # widgets = {
        #     'faculty': forms.ChoiceField(attrs={'class': 'form-control', }),
        # }
        # exclude = ['title']


# Adding models to user fields
class UserUpdateForm(forms.ModelForm):
    username = forms.CharField()

    # email = forms.EmailField() # removed because user shouldnt be able to change email without confirmation

    class Meta:
        model = User
        fields = ['username']  # fields to be updated by user
