# Generated by Django 3.0.3 on 2020-08-11 05:58

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('apply_main', '0023_auto_20200810_1114'),
    ]

    operations = [
        migrations.AddField(
            model_name='apply',
            name='aadhaar_image',
            field=models.ImageField(blank=True, upload_to='aadhaar_image'),
        ),
    ]