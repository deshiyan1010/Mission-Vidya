# Generated by Django 3.0.3 on 2020-08-16 11:11

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('donation_main', '0008_auto_20200816_1617'),
    ]

    operations = [
        migrations.AlterField(
            model_name='images',
            name='mobile_images',
            field=models.ImageField(blank=True, upload_to='donation_main'),
        ),
    ]