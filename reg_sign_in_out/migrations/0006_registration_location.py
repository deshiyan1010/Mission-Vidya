# Generated by Django 3.0.3 on 2020-08-09 02:14

import django.contrib.gis.db.models.fields
from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('reg_sign_in_out', '0005_remove_registration_url'),
    ]

    operations = [
        migrations.AddField(
            model_name='registration',
            name='location',
            field=django.contrib.gis.db.models.fields.PointField(blank=True, null=True, srid=4326, verbose_name='Location'),
        ),
    ]