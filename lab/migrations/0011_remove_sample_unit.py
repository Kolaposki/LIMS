# Generated by Django 3.0.7 on 2021-06-04 09:42

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('lab', '0010_sample_unit'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='sample',
            name='unit',
        ),
    ]
