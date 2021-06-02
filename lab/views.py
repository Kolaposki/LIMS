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
    all_test = None
    # all_test = Test.objects.all().order_by('-updated_at')
    print("all_test ", all_test)
    return render(request, 'all-tests.html', {'all_test': all_test})


@login_required
def new_test(request):
    all_test = None
    print("all_test ", all_test)
    return render(request, 'new-test.html', {'all_test': all_test})


@login_required
def test_requests(request):
    all_test = None
    # all_test = TestRequests.objects.filter(technician=request.user.pk).order_by('-updated_at')
    print("all_test ", all_test)
    return render(request, 'test-requests.html', {'all_test': all_test})


@login_required
def all_reports(request):
    all_test = None
    # all_test = Report.objects.filter(technician=request.user.pk).order_by('-updated_at')
    print("all_test ", all_test)
    return render(request, 'reports.html', {'all_test': all_test})


@login_required
def laboratories(request):
    all_test = None
    # all_test = Laboratory.objects.filter(technician=request.user.pk).order_by('-updated_at')
    print("all_test ", all_test)
    return render(request, 'laboratories.html', {'all_test': all_test})


@login_required
def all_samples(request):
    all_test = None
    # all_sample = Sample.objects.all().order_by('-updated_at')
    print("all_test ", all_test)
    return render(request, 'all-samples.html', {'all_test': all_test})


@login_required
def new_sample(request):
    all_test = None
    print("all_test ", all_test)
    return render(request, 'new-sample.html', {'all_test': all_test})


@login_required
def sample_list(request):
    all_test = None
    print("all_test ", all_test)
    return render(request, 'sample-lists.html', {'all_test': all_test})
