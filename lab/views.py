from django.http import HttpResponse, HttpResponseForbidden, Http404
from django.shortcuts import render, redirect, reverse, get_object_or_404

from .forms import *
from .models import *
from users.models import *
from django.contrib import messages
from django.contrib.auth.decorators import login_required


@login_required
def dashboard(request):
    print("NOW IN DASHBOARD")
    # print("FILES: ", request.FILES)

    return render(request, 'dashboard.html', {'hi': 'hi'})


@login_required
def all_tests(request):
    all_test = Test.objects.all().order_by('-updated_at')
    total = all_test.count()
    print("all_test ", all_test)
    return render(request, 'all-tests.html', {'all_test': all_test, 'total': total, })


@login_required
def new_test(request):
    technician = get_object_or_404(LabTechnician, manager=request.user)  # check

    all_test = None
    form = TestCreationForm(None)
    all_patients = Patient.objects.all()
    all_doctors = Doctor.objects.all()
    all_labs = Laboratory.objects.all()
    all_sample = Sample.objects.all()
    form_err = None
    context = {'form': form, 'all_patients': all_patients, 'all_doctors': all_doctors, 'all_labs': all_labs,
               'technician': technician, 'form_err': form_err, 'all_samples': all_sample, }

    if request.method == 'POST':
        print("POST: ", request.POST)

        form = TestCreationForm(request.POST or None)
        print("Form: ", form)

        if form.is_valid():
            instance = form.save(commit=False)
            instance.technician = technician

            instance.save()
            form.save_m2m()
            messages.success(request, "Test created successfully")

            return redirect('dashboard')
            # return redirect(instance.get_absolute_url())

        else:
            form_err = form.errors
            print("Form not valid: ", form_err)
            context = {'form': form, 'all_patients': all_patients, 'all_doctors': all_doctors, 'all_labs': all_labs,
                       'technician': technician, 'form_err': form_err, 'all_samples': all_sample, }
            messages.error(request, "Please check the Test form")

        return render(request, 'new-test.html', context=context)

    else:
        return render(request, 'new-test.html', context=context)


@login_required
def test_requests(request):
    technician = get_object_or_404(LabTechnician, manager=request.user)  # check
    all_test = TestRequests.objects.filter(technician=technician).order_by('-updated_at')
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
    all_sample = Sample.objects.all().count()
    blood_samples = Sample.objects.filter(type='Blood').union(Sample.objects.filter(
        type='Plasma'), Sample.objects.filter(type='Tissue biopsy'), Sample.objects.filter(
        type='Serum')).count()

    urine_samples = Sample.objects.filter(type='Urine').count()
    fluid_samples = Sample.objects.filter(type='Oral fluid').union(Sample.objects.filter(
        type='Saliva'), Sample.objects.filter(type='Virology swab'), Sample.objects.filter(
        type='Sputum'), Sample.objects.filter(type='Amniotic fluid'), Sample.objects.filter(
        type='Cerebrospinal fluid (CSF)')).count()

    other_samples = Sample.objects.filter(type='Bone marrow').union(Sample.objects.filter(
        type='Semen'), Sample.objects.filter(type='Sweat'), Sample.objects.filter(
        type='Stool')).count()

    print("blood_samples ", blood_samples)
    print("urine_samples ", urine_samples)
    print("fluid_samples ", fluid_samples)
    print("other_samples ", other_samples)
    context = {'all_sample': all_sample, 'blood_samples': blood_samples, 'urine_samples': urine_samples,
               'fluid_samples': fluid_samples,
               'other_samples': other_samples}
    return render(request, 'all-samples.html', context=context)


@login_required
def new_sample(request):
    technician = get_object_or_404(LabTechnician, manager=request.user)  # check

    form = SampleCreationForm(None)
    all_patients = Patient.objects.all()

    form_err = None
    context = {'form': form, 'all_patients': all_patients, 'technician': technician, 'form_err': form_err, }

    if request.method == 'POST':
        print("POST: ", request.POST)

        form = SampleCreationForm(request.POST or None, request.FILES or None)
        print("Form: ", form)

        if form.is_valid():
            instance = form.save(commit=False)
            instance.technician = technician

            instance.save()
            form.save_m2m()
            messages.success(request, "Sample created successfully")

            return redirect('dashboard')
            # return redirect(instance.get_absolute_url())

        else:
            form_err = form.errors
            print("Form not valid: ", form_err)
            context = {'form': form, 'all_patients': all_patients, 'technician': technician, 'form_err': form_err, }

            messages.error(request, "Please check the Sample form")

        return render(request, 'new-sample.html', context=context)

    return render(request, 'new-sample.html', context=context)


@login_required
def sample_list(request, sample_type):
    samples = None
    sample_meta = ''
    print("sample_type: ", sample_type)

    if sample_type.lower() == 'blood':
        samples = Sample.objects.filter(type='Blood').union(Sample.objects.filter(
            type='Plasma'), Sample.objects.filter(type='Tissue biopsy'), Sample.objects.filter(
            type='Serum')).order_by('-collected_on')
        sample_meta = 'Samples related to Blood, Serum, Plasma and Tissue biopsy'

    elif sample_type.lower() == 'urine':
        samples = Sample.objects.filter(type='Urine').order_by('-collected_on')
        sample_meta = 'Samples related to Urine only'

    elif sample_type.lower() == 'fluid':
        samples = Sample.objects.filter(type='Oral fluid').union(Sample.objects.filter(
            type='Saliva'), Sample.objects.filter(type='Virology swab'), Sample.objects.filter(
            type='Sputum'), Sample.objects.filter(type='Amniotic fluid'), Sample.objects.filter(
            type='Cerebrospinal fluid (CSF)')).order_by('-collected_on')
        sample_meta = 'samples related to Oral fluid, Saliva, Amniotic fluid, Cerebrospinal fluid (CSF), Sputum and Virology swab'

    elif sample_type.lower() == 'others':
        samples = Sample.objects.filter(type='Bone marrow').union(Sample.objects.filter(
            type='Semen'), Sample.objects.filter(type='Sweat'), Sample.objects.filter(
            type='Stool')).order_by('-collected_on')
        sample_meta = 'Samples to Bone marrow, Stool, Semen and Sweat'
    else:
        raise Http404

    print("samples ==> ", samples, samples.count())

    context = {'sample_meta': sample_meta, 'sample_type': sample_type, "samples": samples, }

    return render(request, 'sample-lists.html', context=context)


@login_required
def user_settings(request):
    all_test = None
    print("all_test ", all_test)
    return render(request, 'settings.html', {'all_test': all_test})
