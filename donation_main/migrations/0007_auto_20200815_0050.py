# Generated by Django 3.0.3 on 2020-08-14 19:20

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('donation_main', '0006_auto_20200814_2344'),
    ]

    operations = [
        migrations.RenameField(
            model_name='donatedinformation',
            old_name='time',
            new_name='donated_time',
        ),
    ]