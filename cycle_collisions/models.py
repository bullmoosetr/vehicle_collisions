from django.contrib.postgres.fields import ArrayField
from django.db import models

# Create your models here.
class Borough(models.Model):
    created_at = models.DateTimeField(auto_now=True)
    borough = models.CharField(max_length=50)

class CollisionLocation(models.Model):
    zip_code = models.CharField(max_length=6)
    latitude = models.DecimalField(max_digits=10, decimal_places=6)
    longitude = models.DecimalField(max_digits=10, decimal_places=6)
    on_street_name = models.CharField(max_length=100)
    off_street_name = models.CharField(max_length=100)
    cross_street_name = models.CharField(max_length=100)
    borough = models.ForeignKey(
        Borough,
        on_delete=models.CASCADE,
        related_name='collision_location'
    )
    # def __str__(self):
    #     return 'Zip - %s' % (self.zip_code)

class CollisionDetail(models.Model):
    crash_date = models.DateTimeField()
    crash_time = models.TimeField()
    collision_id = models.IntegerField()
    number_of_cyclist_injured = models.IntegerField(null=True)
    contributing_factor_vehicle = ArrayField(
        models.CharField(blank=True, max_length=50)
    )
    vehicle_type_code = ArrayField(
        models.CharField(blank=True, max_length=50)
    )
    collision_location = models.OneToOneField(
        CollisionLocation,
        on_delete=models.CASCADE,
        related_name='collision_detail'
    )
    # def __str__(self):
    #     return '%s %s Injured - %s' % (self.crash_date, self.crash_time, self.number_of_cyclist_injured)

class CitiBikeStation(models.Model):
    station_id = models.FloatField()
    station_name = models.CharField(max_length=100)
    station_latitude = models.DecimalField(max_digits=10, decimal_places=6)
    station_longitude = models.DecimalField(max_digits=10, decimal_places=6)
        