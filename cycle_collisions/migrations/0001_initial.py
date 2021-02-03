# Generated by Django 3.1.5 on 2021-01-31 15:41

import django.contrib.postgres.fields
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Borough',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now=True)),
                ('borough', models.CharField(max_length=50)),
            ],
        ),
        migrations.CreateModel(
            name='CollisionLocation',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('zip_code', models.IntegerField()),
                ('latitude', models.DecimalField(decimal_places=6, max_digits=10)),
                ('longitude', models.DecimalField(decimal_places=6, max_digits=10)),
                ('on_street_name', models.CharField(max_length=100)),
                ('off_street_name', models.CharField(max_length=100)),
                ('cross_street_name', models.CharField(max_length=100)),
                ('borough', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='collision_location', to='cycle_collisions.borough')),
            ],
        ),
        migrations.CreateModel(
            name='CollisionDetail',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('crash_date', models.DateTimeField()),
                ('crash_time', models.TimeField()),
                ('collision_id', models.IntegerField()),
                ('number_of_cyclist_injured', models.IntegerField()),
                ('contributing_factor_vehicle', django.contrib.postgres.fields.ArrayField(base_field=models.CharField(blank=True, max_length=50), size=None)),
                ('vehicle_type_code', django.contrib.postgres.fields.ArrayField(base_field=models.CharField(blank=True, max_length=50), size=None)),
                ('collision_location', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='collision_detail', to='cycle_collisions.collisionlocation')),
            ],
        ),
    ]