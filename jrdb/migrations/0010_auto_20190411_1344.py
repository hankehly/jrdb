# Generated by Django 2.1.7 on 2019-04-11 13:44

import django.contrib.postgres.fields
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('jrdb', '0009_auto_20190410_1404'),
    ]

    operations = [
        migrations.AlterField(
            model_name='jockey',
            name='cur_yr_flat_r',
            field=django.contrib.postgres.fields.ArrayField(base_field=models.PositiveSmallIntegerField(), null=True, size=4),
        ),
        migrations.AlterField(
            model_name='jockey',
            name='cur_yr_obst_r',
            field=django.contrib.postgres.fields.ArrayField(base_field=models.PositiveSmallIntegerField(), null=True, size=4),
        ),
        migrations.AlterField(
            model_name='jockey',
            name='prev_yr_flat_r',
            field=django.contrib.postgres.fields.ArrayField(base_field=models.PositiveSmallIntegerField(), null=True, size=4),
        ),
        migrations.AlterField(
            model_name='jockey',
            name='prev_yr_obst_r',
            field=django.contrib.postgres.fields.ArrayField(base_field=models.PositiveSmallIntegerField(), null=True, size=4),
        ),
        migrations.AlterField(
            model_name='jockey',
            name='sum_flat_r',
            field=django.contrib.postgres.fields.ArrayField(base_field=models.PositiveSmallIntegerField(), null=True, size=4),
        ),
        migrations.AlterField(
            model_name='jockey',
            name='sum_obst_r',
            field=django.contrib.postgres.fields.ArrayField(base_field=models.PositiveSmallIntegerField(), null=True, size=4),
        ),
    ]