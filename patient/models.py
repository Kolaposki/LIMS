from django.db import models
from ehr.models import BaseModel
from django.utils.translation import gettext_lazy as _


# Create your models here.

class Gender(models.TextChoices):
    MALE = 'M', _('Male')
    FEMALE = 'F', _('Female')
    NON_BINARY = 'N', _('Non Binary')
    OTHERS = 'O', _('I Prefer not to Say')


class BloodGroup(models.TextChoices):
    A_POSITIVE = 'A1', _('A+')
    B_POSITIVE = 'B1', _('B+')
    O_POSITIVE = 'O1', _('A+')
    A_NEGATIVE = 'A0', _('A-')
    B_NEGATIVE = 'B0', _('B-')
    O_NEGATIVE = 'O0', _('O-')


class Genotype(models.TextChoices):
    AA = 'AA', _('AA')
    AS = 'AS', _('AS')
    SS = 'SS', _('SS')
    SC = 'SC', _('SC')


class Patient(BaseModel):
    """
        Patient should be gotten through api. Should be added through admin portal
    """

    manager = models.ForeignKey(User, on_delete=models.CASCADE)
    patient_avi = models.ImageField(upload_to=None, height_field=None, width_field=None, max_length=None, blank=True,
                                    null=True)
    patient_no = models.CharField(max_length=50, blank=True, null=True)

    first_name = models.CharField(max_length=50, blank=True, null=True)
    last_name = models.CharField(max_length=50, blank=True, null=True)
    middle_name = models.CharField(max_length=50, blank=True, null=True)
    dob = models.DateField(("Date of Birth"), auto_now=False, auto_now_add=False)
    age = models.CharField(max_length=3, blank=True, null=True)
    gender = models.CharField(
        max_length=1,
        choices=Gender.choices,
        default=Gender.OTHERS,
        blank=True, null=True
    )
    mothers_maiden_name = models.CharField(max_length=50, blank=True, null=True)
    occupation = models.CharField(max_length=50, blank=True, null=True)

    home_address = models.CharField(max_length=100, blank=True, null=True)
    phone_number = models.CharField(max_length=12, blank=True, null=True)
    alt_phone_number = models.CharField(max_length=12, blank=True, null=True)
    email = models.EmailField(_(""), max_length=254, blank=True, null=True)

    blood_group = models.CharField(
        max_length=2,
        choices=BloodGroup.choices,
        blank=True, null=True
    )
    genotype = models.CharField(
        max_length=2,
        choices=Genotype.choices,
        blank=True, null=True
    )
    weight = models.CharField(max_length=50, blank=True, null=True)
    height = models.CharField(max_length=50, blank=True, null=True)
    allergies = models.CharField(max_length=50, blank=True, null=True)
    disable = models.CharField(max_length=50, blank=True, null=True)
    notes = models.TextField(blank=True, null=True)

    other_notes = models.TextField(blank=True, null=True)
