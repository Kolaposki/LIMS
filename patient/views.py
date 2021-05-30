from django.shortcuts import render


# Create your views here.
def patients(request):
    template = 'patients.html'

    return render(request, 'patients.html')


def add_patient(request):
    template = 'patient_form.html'

    return render(request, template)
