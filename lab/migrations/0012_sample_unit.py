# Generated by Django 3.0.7 on 2021-06-04 09:44

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('lab', '0011_remove_sample_unit'),
    ]

    operations = [
        migrations.AddField(
            model_name='sample',
            name='unit',
            field=models.CharField(choices=[('Grams (g)', 'Grams (g)'), ('Grams per deciliter (g/dL)', 'Grams per deciliter (g/dL)'), ('Grams per liter (g/L)', 'Grams per liter (g/L)'), ('International units per liter (IU/L)', 'International units per liter (IU/L)'), ('International units per milliliter (IU/mL)', 'International units per milliliter (IU/mL)'), ('Micrograms (mcg)', 'Micrograms (mcg)'), ('Micrograms per deciliter (mcg/dL)', 'Micrograms per deciliter (mcg/dL)'), ('Micrograms per liter (mcg/L)', 'Micrograms per liter (mcg/L)'), ('Microkatals per liter (mckat/L)', 'Microkatals per liter (mckat/L)'), ('Microliters (mcL)', 'Microliters (mcL)'), ('Micromoles per liter (mcmol/L)', 'Micromoles per liter (mcmol/L)'), ('Milliequivalents (mEq)', 'Milliequivalents (mEq)'), ('Milliequivalents per liter (mEq/L)', 'Milliequivalents per liter (mEq/L)'), ('Milligrams (mg)', 'Milligrams (mg)'), ('Milligrams per deciliter (mg/dL)', 'Milligrams per deciliter (mg/dL)'), ('Milligrams per liter (mg/L)', 'Milligrams per liter (mg/L)'), ('Milli-international units per liter (mIU/L)', 'Milli-international units per liter (mIU/L)'), ('Milliliters (mL)', 'Milliliters (mL)'), ('Millimeters (mm)', 'Millimeters (mm)'), ('Millimeters of mercury (mm Hg)', 'Millimeters of mercury (mm Hg)'), ('Millimoles (mmol)', 'Millimoles (mmol)'), ('Millimoles per liter (mmol/L)', 'Millimoles per liter (mmol/L)'), ('Milliosmoles per kilogram of water (mOsm/kg water)', 'Milliosmoles per kilogram of water (mOsm/kg water)'), ('Milliunits per gram (mU/g)', 'Milliunits per gram (mU/g)'), ('Milliunits per liter (mU/L)', 'Milliunits per liter (mU/L)'), ('Nanograms per deciliter (ng/dL)', 'Nanograms per deciliter (ng/dL)'), ('Nanograms per liter (ng/L)', 'Nanograms per liter (ng/L)'), ('Nanograms per milliliter (ng/mL)', 'Nanograms per milliliter (ng/mL)'), ('Nanograms per milliliter per hour (ng/mL/hr)', 'Nanograms per milliliter per hour (ng/mL/hr)'), ('Nanomoles (nmol)', 'Nanomoles (nmol)'), ('Nanomoles per liter (nmol/L)', 'Nanomoles per liter (nmol/L)'), ('Picograms (pg)', 'Picograms (pg)'), ('Picograms per milliliter (pg/mL)', 'Picograms per milliliter (pg/mL)'), ('Picomoles per liter (pmol/L)', 'Picomoles per liter (pmol/L)'), ('Units per liter (U/L)', 'Units per liter (U/L)'), ('Units per milliliter (U/mL)', 'Units per milliliter (U/mL)'), ('Titers', 'Titers')], default='Grams per deciliter (g/dL)', max_length=100),
        ),
    ]
