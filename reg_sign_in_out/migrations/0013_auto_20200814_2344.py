# Generated by Django 3.0.3 on 2020-08-14 18:14

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('reg_sign_in_out', '0012_auto_20200814_0445'),
    ]

    operations = [
        migrations.AlterField(
            model_name='registration',
            name='profile_pic',
            field=models.ImageField(blank=True, upload_to='profile_pic'),
        ),
    ]
