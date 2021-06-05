import datetime
from django.db import models
import uuid, os, random, string
from django.contrib.auth.models import User
from django.urls import reverse
from taggit.managers import TaggableManager
from shortuuidfield import ShortUUIDField
from patient.models import Patient
from django_resized import ResizedImageField
from ckeditor.fields import RichTextField

TEST_UNITS = (
    ("Grams (g)", "Grams (g)"),
    ("Grams per deciliter (g/dL)", "Grams per deciliter (g/dL)"),
    ("Grams per liter (g/L)", "Grams per liter (g/L)"),
    ("International units per liter (IU/L)", "International units per liter (IU/L)"),
    ("International units per milliliter (IU/mL)", "International units per milliliter (IU/mL)"),
    ("Micrograms (mcg)", "Micrograms (mcg)"),
    ("Micrograms per deciliter (mcg/dL)", "Micrograms per deciliter (mcg/dL)"),
    ("Micrograms per liter (mcg/L)", "Micrograms per liter (mcg/L)"),
    ("Microkatals per liter (mckat/L)", "Microkatals per liter (mckat/L)"),
    ("Microliters (mcL)", "Microliters (mcL)"),
    ("Micromoles per liter (mcmol/L)", "Micromoles per liter (mcmol/L)"),
    ("Milliequivalents (mEq)", "Milliequivalents (mEq)"),
    ("Milliequivalents per liter (mEq/L)", "Milliequivalents per liter (mEq/L)"),
    ("Milligrams (mg)", "Milligrams (mg)"),
    ("Milligrams per deciliter (mg/dL)", "Milligrams per deciliter (mg/dL)"),
    ("Milligrams per liter (mg/L)", "Milligrams per liter (mg/L)"),
    ("Milli-international units per liter (mIU/L)", "Milli-international units per liter (mIU/L)"),
    ("Milliliters (mL)", "Milliliters (mL)"),
    ("Millimeters (mm)", "Millimeters (mm)"),
    ("Millimeters of mercury (mm Hg)", "Millimeters of mercury (mm Hg)"),
    ("Millimoles (mmol)", "Millimoles (mmol)"),
    ("Millimoles per liter (mmol/L)", "Millimoles per liter (mmol/L)"),
    ("Milliosmoles per kilogram of water (mOsm/kg water)", "Milliosmoles per kilogram of water (mOsm/kg water)"),
    ("Milliunits per gram (mU/g)", "Milliunits per gram (mU/g)"),
    ("Milliunits per liter (mU/L)", "Milliunits per liter (mU/L)"),
    ("Nanograms per deciliter (ng/dL)", "Nanograms per deciliter (ng/dL)"),
    ("Nanograms per liter (ng/L)", "Nanograms per liter (ng/L)"),
    ("Nanograms per milliliter (ng/mL)", "Nanograms per milliliter (ng/mL)"),
    ("Nanograms per milliliter per hour (ng/mL/hr)", "Nanograms per milliliter per hour (ng/mL/hr)"),
    ("Nanomoles (nmol)", "Nanomoles (nmol)"),
    ("Nanomoles per liter (nmol/L)", "Nanomoles per liter (nmol/L)"),
    ("Picograms (pg)", "Picograms (pg)"),
    ("Picograms per milliliter (pg/mL)", "Picograms per milliliter (pg/mL)"),
    ("Picomoles per liter (pmol/L)", "Picomoles per liter (pmol/L)"),
    ("Units per liter (U/L)", "Units per liter (U/L)"),
    ("Units per milliliter (U/mL)", "Units per milliliter (U/mL)"),
    ("Titers", "Titers"),
)

HELP_TEXT = {
    'queries': "Information about the person and blood sample. Any pertinent information regarding the patient’s test preparation or the condition of specimen may be noted here.",
}

TEST_STATUS = (
    ("Routine", "Routine"),
    ("STAT", "STAT"),
    # Status of the test request, such as Routine or STAT (perform test as rapidly as possible).
)

TEST_REQUEST_STATE = (
    ("Ordered", "Ordered"),
    ("Draft", "Draft"),
    # Status of the test request, such as Routine or STAT (perform test as rapidly as possible).
)

LAB_DEPARTMENTS = (
    ("Chemistry", "Chemistry"),
    ("Hematology", "Hematology"),
    ("Microbiology", "Microbiology"),
    ("Transfusion Services", "Transfusion Services"),
    ("Immunology", "Immunology"),
    ("Cytology", "Cytology"),
    ("Coagulation", "Coagulation"),
    ("Urinalysis", "Urinalysis"),
    ("Surgical Pathology", "Surgical Pathology"),

)

TEST_CATEGORY = (
    ("Complete Blood Count", "Complete Blood Count"),
    ("Prothrombin Time", "Prothrombin Time"),
    ("Basic Metabolic Panel", "Basic Metabolic Panel"),
    ("Comprehensive Metabolic Panel", "Comprehensive Metabolic Panel"),
    ("Lipid Panel", "Lipid Panel"),
    ("Liver Panel", "Liver Panel"),
    ("Thyroid Stimulating Hormone", "Thyroid Stimulating Hormone"),
    ("Hemoglobin A1C", "Hemoglobin A1C"),
    ("Urinalysis", "Urinalysis"),
    ("Culture", "Culture"),
    ("Thyroid Profile III", "Thyroid Profile III"),
    ("Activated Partial Thromboplastin Time", "Activated Partial Thromboplastin Time"),
    ("Lipid Profile", "Lipid Profile"),
)

SAMPLE_TYPES = (
    ("Blood", "Blood"),
    ("Serum", "Serum"),
    ("Sweat", "Sweat"),
    ("Oral fluid", "Oral fluid"),
    ("Saliva", "Saliva"),
    ("Urine", "Urine"),
    ("Amniotic fluid", "Amniotic fluid"),
    ("Bone marrow", "Bone marrow"),
    ("Cerebrospinal fluid (CSF)", "Cerebrospinal fluid (CSF)"),
    ("Tissue biopsy", "Tissue biopsy"),
    ("Stool", "Stool"),
    ("Sputum", "Sputum"),
    ("Semen", "Semen"),
    ("Virology swab", "Virology swab"),
    ("Plasma", "Plasma"),
)


def sample_image_directory_path(instance, filename):
    return f'sample_images/{instance.type}_{instance.collected_on}'


class LabTechnician(models.Model):
    """
        Humans that are in charge of uploading lab tests and others
    """
    manager = models.ForeignKey(User, on_delete=models.CASCADE)
    slug = models.UUIDField(default=uuid.uuid4, editable=False, blank=True, null=True)
    created_at = models.DateTimeField(null=True, auto_now_add=True)
    updated_at = models.DateTimeField(null=True, auto_now=True)
    uuid = ShortUUIDField(max_length=5, editable=False, null=True, blank=True)

    def __str__(self):
        return f"Technician {self.manager.first_name} {self.manager.last_name}"

    def full_name(self):
        return f'{self.manager.last_name} {self.manager.first_name}'

    class Meta:
        ordering = ['-created_at']
        verbose_name_plural = "Lab Technicians"  # A human-readable name for the object, plural


class Doctor(models.Model):
    """
        Doc that approved the test
    """
    # manager = models.ForeignKey(User, on_delete=models.CASCADE)

    first_name = models.CharField(max_length=50, blank=True, null=True)
    last_name = models.CharField(max_length=50, blank=True, null=True)
    other_name = models.CharField(max_length=50, blank=True, null=True)

    slug = models.UUIDField(default=uuid.uuid4, editable=False, blank=True, null=True)
    created_at = models.DateTimeField(null=True, auto_now_add=True)
    updated_at = models.DateTimeField(null=True, auto_now=True)
    uuid = ShortUUIDField(max_length=5, editable=False, null=True, blank=True)

    def __str__(self):
        return f"Doctor {self.last_name} {self.first_name}"

    def full_name(self):
        return f'{self.last_name} {self.first_name}'

    class Meta:
        ordering = ['-created_at']


class Laboratory(models.Model):
    """
    Physical labs where tests are carried out
    """
    departments = models.CharField(choices=LAB_DEPARTMENTS, max_length=100, null=True, blank=True)
    location = models.CharField(max_length=200)
    slug = models.UUIDField(default=uuid.uuid4, editable=False, blank=True, null=True)
    uuid = ShortUUIDField(max_length=5, editable=False, null=True, blank=True)

    def __str__(self):
        return f"{self.departments} Lab"

    class Meta:
        verbose_name_plural = "Laboratories"  # A human-readable name for the object, plural


class Sample(models.Model):
    """
        Physical samples that were collected to be examined in the lab
    """

    type = models.CharField(choices=SAMPLE_TYPES, max_length=100, null=True, blank=True)
    name = models.CharField(max_length=200)
    patient = models.ForeignKey(Patient, on_delete=models.CASCADE)  # patient whom the sample was requested for

    slug = models.UUIDField(default=uuid.uuid4, editable=False, blank=True, null=True)
    notes = models.TextField(null=True, blank=True)
    quantity = models.FloatField(blank=True, null=True)
    collected_on = models.DateTimeField(null=True, auto_now_add=True)
    uuid = ShortUUIDField(max_length=5, editable=False, null=True, blank=True)
    image1 = ResizedImageField(size=[500, 300], quality=100, upload_to=sample_image_directory_path, null=True,
                               blank=True)
    image2 = ResizedImageField(size=[500, 300], quality=100, upload_to=sample_image_directory_path, null=True,
                               blank=True)
    unit = models.CharField(choices=TEST_UNITS, max_length=100, default='Grams per deciliter (g/dL)')

    def __str__(self):
        return f"{self.type} sample"

    def full_details(self):
        return f'{self.name} - {self.type}'

    def short_slug(self):
        return f'{self.uuid[0:5]}'

    def measurement(self):
        return f'{self.quantity} {self.unit}'


class Test(models.Model):
    """
        Test that would be/was carried out.
    """
    technician = models.ForeignKey(LabTechnician, on_delete=models.CASCADE)
    lab = models.ForeignKey(Laboratory, on_delete=models.CASCADE)
    sample = models.ForeignKey(Sample, on_delete=models.CASCADE)
    patient = models.ForeignKey(Patient, on_delete=models.CASCADE)  # patient whom the test was carried on
    doctor = models.ForeignKey(Doctor, on_delete=models.CASCADE)  # doc who approved the test

    name = models.CharField(max_length=200)
    category = models.CharField(choices=TEST_CATEGORY, max_length=100, null=True, blank=True)
    code = models.CharField(help_text="Example: CBC, BMB", max_length=80)

    status = models.CharField(choices=TEST_STATUS, max_length=50, null=True, blank=True)
    notes = models.TextField(null=True, blank=True)
    queries = models.TextField(help_text=HELP_TEXT.get('queries'), null=True, blank=True)
    description = RichTextField(blank=True)
    created_at = models.DateTimeField(null=True, auto_now_add=True)
    updated_at = models.DateTimeField(null=True, auto_now=True)
    tags = TaggableManager(blank=True)

    rate = models.DecimalField(blank=True, null=True, max_digits=5, decimal_places=2)
    upper_bound = models.DecimalField(blank=True, null=True, max_digits=5, decimal_places=2)
    lower_bound = models.DecimalField(blank=True, null=True, max_digits=5, decimal_places=2)
    charges = models.DecimalField(help_text="in dollars", blank=True, null=True, max_digits=5, decimal_places=2)
    duration = models.FloatField(help_text="in minutes", blank=True, null=True)  # in minutes
    unit = models.CharField(choices=TEST_UNITS, max_length=100, null=True, blank=True)
    date_initiated = models.DateField(blank=False, null=False, default=datetime.date.today)
    date_completed = models.DateField(blank=False, null=False, default=datetime.date.today)
    slug = models.UUIDField(default=uuid.uuid4, editable=False, blank=True, null=True)
    uuid = ShortUUIDField(max_length=5, editable=False, null=True, blank=True)

    def __str__(self):
        return f"Test-{self.code}"

    def short_slug(self):
        return f'{self.uuid[0:5]}'

    def get_absolute_url(self):
        return reverse("test_details", args=[str(self.uuid)])


class TestRequests(models.Model):
    """
        Test that was requested by a doctor.
    """
    technician = models.ForeignKey(LabTechnician, on_delete=models.CASCADE)  # technician whom the test was assigned to
    sample = models.ForeignKey(Sample, on_delete=models.CASCADE)
    patient = models.ForeignKey(Patient, on_delete=models.CASCADE)  # patient whom the test was requested for
    doctor = models.ForeignKey(Doctor, on_delete=models.CASCADE)  # doc who gave out the test

    category = models.CharField(choices=TEST_CATEGORY, max_length=100, null=True, blank=True)
    state = models.CharField(choices=TEST_REQUEST_STATE, max_length=50, null=True, blank=True)
    description = models.TextField(null=True, blank=True)
    is_urgent = models.BooleanField(default=False)

    created_at = models.DateTimeField(null=True, auto_now_add=True)
    updated_at = models.DateTimeField(null=True, auto_now=True)

    slug = models.UUIDField(default=uuid.uuid4, editable=False, blank=True, null=True)
    uuid = ShortUUIDField(max_length=5, editable=False, null=True, blank=True)

    def __str__(self):
        return f"TestRequest-{self.category}"

    def short_slug(self):
        return f'{self.uuid[0:5]} '


# TODO : should generate a pdf
class Report(models.Model):
    """
        Report contains all elements as mandated by federal legislation known as the Clinical Laboratory Improvement Amendments (CLIA).

        https://labtestsonline.org/articles/how-to-read-your-laboratory-report
    """

    test = models.ForeignKey(Test, on_delete=models.CASCADE)

    title = models.CharField(max_length=200)
    generated_at = models.DateTimeField(null=True, auto_now_add=True)  # date report was generated.

    type = models.CharField(choices=SAMPLE_TYPES, max_length=100, null=True, blank=True)
    slug = models.UUIDField(default=uuid.uuid4, editable=False, blank=True, null=True)
    comment = models.TextField(null=True, blank=True)
    quantity = models.FloatField(blank=True, null=True)
    uuid = ShortUUIDField(max_length=5, editable=False, null=True, blank=True)

    def __str__(self):
        return f"{self.type} report"
