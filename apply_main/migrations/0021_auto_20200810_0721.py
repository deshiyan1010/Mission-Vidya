# Generated by Django 3.0.3 on 2020-08-10 07:21

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('apply_main', '0020_apply_special_key'),
    ]

    operations = [
        migrations.AlterField(
            model_name='apply',
            name='aadhaar_number',
            field=models.CharField(max_length=12, unique=True),
        ),
        migrations.AlterField(
            model_name='apply',
            name='phone_number',
            field=models.CharField(max_length=10),
        ),
    ]