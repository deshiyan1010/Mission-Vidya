# Generated by Django 3.0.3 on 2020-08-13 04:15

from django.db import migrations
import smartfields.fields


class Migration(migrations.Migration):

    dependencies = [
        ('reg_sign_in_out', '0010_auto_20200810_1222'),
    ]

    operations = [
        migrations.AlterField(
            model_name='registration',
            name='profile_pic',
            field=smartfields.fields.ImageField(upload_to='profile_pic'),
        ),
    ]
