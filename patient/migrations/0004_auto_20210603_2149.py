# Generated by Django 3.0.7 on 2021-06-03 20:49

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('patient', '0003_auto_20210603_1811'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='patient',
            name='manager',
        ),
        migrations.AddField(
            model_name='patient',
            name='first_name',
            field=models.CharField(blank=True, max_length=50, null=True),
        ),
        migrations.AddField(
            model_name='patient',
            name='last_name',
            field=models.CharField(blank=True, max_length=50, null=True),
        ),
        migrations.AddField(
            model_name='patient',
            name='other_name',
            field=models.CharField(blank=True, max_length=50, null=True),
        ),
    ]