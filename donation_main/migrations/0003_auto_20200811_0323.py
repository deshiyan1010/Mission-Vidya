# Generated by Django 3.0.3 on 2020-08-11 03:23

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('apply_main', '0023_auto_20200810_1114'),
        ('donation_main', '0002_auto_20200805_1229'),
    ]

    operations = [
        migrations.AddField(
            model_name='donate',
            name='donated',
            field=models.BooleanField(default=False),
        ),
        migrations.CreateModel(
            name='DonatedInformation',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('device', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='donation_main.Donate')),
                ('receiver', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='apply_main.Apply')),
            ],
        ),
    ]
