# Generated by Django 3.0.3 on 2020-08-05 10:56

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Apply',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('first_name', models.CharField(max_length=64)),
                ('middle_name', models.CharField(blank=True, max_length=64)),
                ('last_name', models.CharField(max_length=64)),
                ('published', models.DateTimeField(auto_now_add=True)),
            ],
        ),
    ]
