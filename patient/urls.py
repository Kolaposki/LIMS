from django.urls import path, include
from . import views

urlpatterns = [
    path('', views.patients, name='patients'),
    path('add_patient', views.add_patient, name='add_patient')
]
