# Generated by Django 3.0.3 on 2020-08-12 09:13

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('donation_main', '0003_auto_20200811_0323'),
    ]

    operations = [
        migrations.AddField(
            model_name='donatedinformation',
            name='time',
            field=models.DateTimeField(auto_now_add=True, default=django.utils.timezone.now),
            preserve_default=False,
        ),
    ]
