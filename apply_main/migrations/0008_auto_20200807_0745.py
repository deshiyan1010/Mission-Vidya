# Generated by Django 3.0.3 on 2020-08-07 07:45

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('apply_main', '0007_auto_20200807_0743'),
    ]

    operations = [
        migrations.AlterField(
            model_name='apply',
            name='middle_name',
            field=models.CharField(blank=True, max_length=64, null=True),
        ),
    ]