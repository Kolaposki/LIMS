# Generated by Django 3.0.7 on 2021-06-04 07:47

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('patient', '0004_auto_20210603_2149'),
        ('lab', '0007_auto_20210604_0358'),
    ]

    operations = [
        migrations.AddField(
            model_name='sample',
            name='patient',
            field=models.ForeignKey(default=2, on_delete=django.db.models.deletion.CASCADE, to='patient.Patient'),
            preserve_default=False,
        ),
    ]
