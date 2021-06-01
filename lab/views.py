from django.http import HttpResponse, HttpResponseForbidden
from django.shortcuts import render, redirect, reverse, get_object_or_404

from .forms import *
from .models import *
from users.models import *
from django.contrib import messages
from django.contrib.auth.decorators import login_required


@login_required
def dashboard(request):
    print("NOW IN DASHBOARD")
    print("FILES: ", request.FILES)

    return render(request, 'dashboard.html', {'hi': 'hi'})


@login_required
def all_tests(request):
    all_test = Test.objects.all().order_by('-updated_at')
    print("all_test ", all_test)
    return render(request, 'all-tests.html', {'all_test': all_test})
