# Generated by Django 3.0.3 on 2020-08-06 10:31

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('apply_main', '0004_auto_20200806_0938'),
    ]

    operations = [
        migrations.AlterField(
            model_name='apply',
            name='lat',
            field=models.FloatField(),
        ),
        migrations.AlterField(
            model_name='apply',
            name='lon',
            field=models.FloatField(),
        ),
    ]