# Generated by Django 3.0.3 on 2020-08-14 17:03

from django.db import migrations
import smartfields.fields


class Migration(migrations.Migration):

    dependencies = [
        ('donation_main', '0004_donatedinformation_time'),
    ]

    operations = [
        migrations.AlterField(
            model_name='images',
            name='mobile_images',
            field=smartfields.fields.ImageField(upload_to='donation_main'),
        ),
    ]
