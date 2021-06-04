from .models import *
from django import forms


class TestCreationForm(forms.ModelForm):
    class Meta:
        model = Test
        fields = '__all__'
        exclude = ['created_at', 'updated_at', 'technician',]
