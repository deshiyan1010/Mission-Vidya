# Generated by Django 3.0.3 on 2020-08-05 12:29

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('donation_main', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='donate',
            name='model_name',
            field=models.CharField(max_length=264),
        ),
    ]