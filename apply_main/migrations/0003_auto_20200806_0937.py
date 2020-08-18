# Generated by Django 3.0.3 on 2020-08-06 09:37

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('apply_main', '0002_auto_20200806_0913'),
    ]

    operations = [
        migrations.AddField(
            model_name='apply',
            name='aadhaar_number',
            field=models.IntegerField(default=235436, unique=True),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='apply',
            name='district',
            field=models.ForeignKey(default='', on_delete=django.db.models.deletion.CASCADE, to='apply_main.District'),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='apply',
            name='dob',
            field=models.DateField(default='2000-01-01'),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='apply',
            name='lat',
            field=models.IntegerField(default=1),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='apply',
            name='lon',
            field=models.IntegerField(default=1),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='apply',
            name='state',
            field=models.ForeignKey(default='', on_delete=django.db.models.deletion.CASCADE, to='apply_main.State'),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='apply',
            name='subdistrict',
            field=models.ForeignKey(default='', on_delete=django.db.models.deletion.CASCADE, to='apply_main.Subdistrict'),
            preserve_default=False,
        ),
    ]
