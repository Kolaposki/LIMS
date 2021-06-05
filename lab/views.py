from django.http import HttpResponse, HttpResponseForbidden, Http404
from django.shortcuts import render, redirect, reverse, get_object_or_404

from .forms import *
from .models import *
from users.models import *
from django.contrib import messages
from django.contrib.auth.decorators import login_required


@login_required
def dashboard(request):
    technician = get_object_or_404(LabTechnician, manager=request.user)  # check

    print("NOW IN DASHBOARD")
    # print("FILES: ", request.FILES)

    return render(request, 'dashboard.html', {'hi': 'hi'})


@login_required
def all_tests(request):
    technician = get_object_or_404(LabTechnician, manager=request.user)  # check
    all_test = Test.objects.filter(technician=technician).order_by('-updated_at')
    print("all_test ", all_test)
    total = all_test.count()
    return render(request, 'all-tests.html', {'all_test': all_test, 'total': total, })


@login_required
def test_details(request, test_uuid):
    technician = get_object_or_404(LabTechnician, manager=request.user)  # check
    test_obj = get_object_or_404(Test, uuid=test_uuid)

    print("test_obj ", test_obj)
    context = {"test_obj": test_obj}
    return render(request, 'test-details.html', context=context)


@login_required
def update_test(request, test_uuid):
    technician = get_object_or_404(LabTechnician, manager=request.user)  # check
    test_obj = get_object_or_404(Test, uuid=test_uuid)
    tags = test_obj.tags.names()
    print("tags: ", tags)

    all_test = None
    form = TestCreationForm(request.POST or None, instance=test_obj)
    print("TestCreationForm: ", form)

    all_patients = Patient.objects.all()
    all_doctors = Doctor.objects.all()
    all_labs = Laboratory.objects.all()
    all_sample = Sample.objects.all()
    form_err = None
    context = {'form': form, 'all_patients': all_patients, 'all_doctors': all_doctors, 'all_labs': all_labs,
               'technician': technician, 'form_err': form_err, 'all_samples': all_sample, 'tags': tags}

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

            return redirect(instance.get_absolute_url())

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
def new_test(request):
    technician = get_object_or_404(LabTechnician, manager=request.user)  # check
    print("request/; ", request.GET)
    pre_sample = None
    sample_pk = request.GET.get('sample_pk')
    print("sample_pk: ", sample_pk)
    if sample_pk:
        try:
            pre_sample = Sample.objects.get(pk=int(sample_pk))
            print("pre_sample: ", pre_sample)

        except Sample.DoesNotExist:
            print("No pre_sample")

    all_test = None
    form = TestCreationForm(None)
    all_patients = Patient.objects.all()
    all_doctors = Doctor.objects.all()
    all_labs = Laboratory.objects.all()
    all_sample = Sample.objects.all()

    form_err = None
    context = {'form': form, 'all_patients': all_patients, 'all_doctors': all_doctors, 'all_labs': all_labs,
               'technician': technician, 'form_err': form_err, 'all_samples': all_sample, 'pre_sample': pre_sample}

    if request.method == 'POST':
        print("POST: ", request.POST)

        form = TestCreationForm(request.POST or None)
        print("Form: ", form)

        if form.is_valid():
            check_sample = form.cleaned_data.get('sample')
            print("check_Sample: ", check_sample)
            check_sample_obj = check_sample.patient_id
            check_patient_pk = form.cleaned_data.get('patient')

            print("check_sample_obj ::> ", check_sample_obj)
            print("check_patient_pk ::> ", check_patient_pk.pk)

            if check_patient_pk.pk == check_sample_obj:
                print("patient_check is valid: ")
                pass

            else:
                print("Patient in sample differs from patient selected")

                check_message = f"The patient selected '{check_patient_pk.full_name()}' is different from the sample's patient selected '{check_sample.patient.full_name()}'. "

                context = {'form': form, 'all_patients': all_patients, 'all_doctors': all_doctors, 'all_labs': all_labs,
                           'technician': technician, 'form_err': form_err, 'all_samples': all_sample,
                           'patient_check': True, 'check_message': check_message}
                return render(request, 'new-test.html', context=context)

            instance = form.save(commit=False)
            instance.technician = technician

            instance.save()
            form.save_m2m()
            messages.success(request, "Test created successfully")

            return redirect(instance.get_absolute_url())

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
def reject_test_requests(request, test_uuid):
    technician = get_object_or_404(LabTechnician, manager=request.user)  # check
    request_obj = get_object_or_404(TestRequests, uuid=test_uuid)
    request_obj.delete()
    print("Test rejected successfully")
    messages.info(request, "Test rejected successfully")
    return redirect('dashboard', permanent=True)


@login_required
def test_requests_details(request, test_uuid):
    technician = get_object_or_404(LabTechnician, manager=request.user)  # check
    request_obj = get_object_or_404(TestRequests, uuid=test_uuid)

    print("request_obj ", request_obj)
    context = {"request_obj": request_obj}
    return render(request, 'test-request-details.html', context=context)


@login_required
def all_reports(request):
    all_test = None
    # all_test = Report.objects.filter(technician=request.user.pk).order_by('-updated_at')
    print("all_test ", all_test)
    return render(request, 'reports.html', {'all_test': all_test})


@login_required
def laboratories(request):
    all_test = None
    technician = get_object_or_404(LabTechnician, manager=request.user)  # check
    chemistry_tests = Test.objects.filter(lab__departments="Chemistry").count()
    hematology_tests = Test.objects.filter(lab__departments="Hematology").count()
    microbiology_tests = Test.objects.filter(lab__departments="Microbiology").count()
    trans_services_tests = Test.objects.filter(lab__departments="Transfusion Services").count()
    immunology_tests = Test.objects.filter(lab__departments="Immunology").count()
    cytology_tests = Test.objects.filter(lab__departments="Cytology").count()
    coagulation_tests = Test.objects.filter(lab__departments="Coagulation").count()
    urinalysis_tests = Test.objects.filter(lab__departments="Urinalysis").count()
    surgical_tests = Test.objects.filter(lab__departments="Surgical Pathology").count()

    context = {"chemistry_tests": chemistry_tests, "surgical_tests": surgical_tests,
               "urinalysis_tests": urinalysis_tests, "coagulation_tests": coagulation_tests,
               "cytology_tests": cytology_tests, "immunology_tests": immunology_tests,
               "trans_services_tests": trans_services_tests,
               "microbiology_tests": microbiology_tests, "hematology_tests": hematology_tests, }
    return render(request, 'laboratories.html', context=context)


@login_required
def lab_tests(request, department):
    technician = get_object_or_404(LabTechnician, manager=request.user)  # check
    department = department.title()
    print("department  ==>", department)
    lab_obj = get_object_or_404(Laboratory, departments=department)  # check
    all_lab_tests = Test.objects.filter(technician=technician).filter(lab=lab_obj).order_by('-updated_at')

    print("all_lab_tests ", all_lab_tests)
    total = all_lab_tests.count()
    return render(request, 'lab-tests.html', {'all_lab_tests': all_lab_tests, 'total': total, 'department': department})


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
            instance.save()
            messages.success(request, "Sample created successfully")
            return redirect(instance.get_absolute_url())

        else:
            form_err = form.errors
            print("Form not valid: ", form_err)
            context = {'form': form, 'all_patients': all_patients, 'technician': technician, 'form_err': form_err, }

            messages.error(request, "Please check the Sample form")

        return render(request, 'new-sample.html', context=context)

    return render(request, 'new-sample.html', context=context)


@login_required
def sample_details(request, sample_uuid):
    technician = get_object_or_404(LabTechnician, manager=request.user)  # check
    sample_obj = get_object_or_404(Sample, uuid=sample_uuid)

    print("sample_obj ", sample_obj)
    context = {"sample_obj": sample_obj}
    return render(request, 'sample-details.html', context=context)


@login_required
def update_sample(request, sample_uuid):
    technician = get_object_or_404(LabTechnician, manager=request.user)  # check
    sample_obj = get_object_or_404(Sample, uuid=sample_uuid)

    form = SampleCreationForm(request.POST or None, request.FILES or None, instance=sample_obj)
    all_patients = Patient.objects.all()

    form_err = None
    context = {'form': form, 'all_patients': all_patients, 'technician': technician, 'form_err': form_err, }

    if request.method == 'POST':
        print("POST: ", request.POST)

        form = SampleCreationForm(request.POST or None, request.FILES or None)
        print("Form: ", form)

        if form.is_valid():
            instance = form.save(commit=False)
            instance.save()
            messages.success(request, "Sample created successfully")
            return redirect(instance.get_absolute_url())

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
