from django_resized import ResizedImageField
from django.contrib.auth.models import User
from django.db import models
from shortuuidfield import ShortUUIDField

from django.db import models
from django.utils import timezone
from django.urls import reverse


def patient_image_directory_path(instance, filename):
    return f'patients/{instance.type}_{instance.collected_on}'


GENDER = (
    ("Male", "Male"),
    ("Female", "Female"),
)

BLOODGROUP = (
    ("A+", "A+"),
    ("B+", "B+"),
    ("A-", "A-"),
    ("B-", "B-"),
    ("O-", "O-"),
    ("O+", "O+"),
)

GENOTYPE = (
    ("AA", "AA"),
    ("AS", "AS"),
    ("SS", "SS"),
    ("SC", "SC"),
)


class Patient(models.Model):
    """
        Patient should be gotten through api. Should be added through admin portal
    """

    first_name = models.CharField(max_length=50, blank=True, null=True)  # todo : to be removed
    last_name = models.CharField(max_length=50, blank=True, null=True)  # todo : to be removed
    other_name = models.CharField(max_length=50, blank=True, null=True)  # todo : to be removed

    # manager = models.ForeignKey(User, on_delete=models.CASCADE)
    patient_avi = ResizedImageField(size=[500, 300], quality=100, upload_to=patient_image_directory_path, null=True,
                                    blank=True)
    dob = models.DateField(auto_now=False, auto_now_add=False)
    age = models.CharField(max_length=3, blank=True, null=True)
    gender = models.CharField(choices=GENDER, max_length=50, null=True, blank=True)
    mothers_maiden_name = models.CharField(max_length=50, blank=True, null=True)
    occupation = models.CharField(max_length=50, blank=True, null=True)

    home_address = models.CharField(max_length=100, blank=True, null=True)
    phone_number = models.CharField(max_length=12, blank=True, null=True)
    alt_phone_number = models.CharField(max_length=12, blank=True, null=True)

    blood_group = models.CharField(choices=BLOODGROUP, max_length=2, null=True, blank=True)
    genotype = models.CharField(choices=GENOTYPE, max_length=2, null=True, blank=True)

    weight = models.CharField(max_length=50, blank=True, null=True)
    height = models.CharField(max_length=50, blank=True, null=True)
    allergies = models.CharField(max_length=50, blank=True, null=True)
    disable = models.CharField(max_length=50, blank=True, null=True)
    notes = models.TextField(blank=True, null=True)

    created_at = models.DateTimeField(null=True, auto_now_add=True)
    updated_at = models.DateTimeField(null=True, auto_now=True)
    uuid = ShortUUIDField(max_length=5, editable=False, null=True, blank=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return f"Patient {self.last_name} {self.first_name}"

    def full_name(self):
        return f'{self.last_name} {self.first_name}'
