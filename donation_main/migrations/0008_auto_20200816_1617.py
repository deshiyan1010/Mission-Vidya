# Generated by Django 3.0.3 on 2020-08-16 10:47

from django.db import migrations
import s3direct.fields


class Migration(migrations.Migration):

    dependencies = [
        ('donation_main', '0007_auto_20200815_0050'),
    ]

    operations = [
        migrations.AlterField(
            model_name='images',
            name='mobile_images',
            field=s3direct.fields.S3DirectField(blank=True),
        ),
    ]
