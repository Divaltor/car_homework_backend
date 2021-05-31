from django.contrib.auth.models import AbstractUser
from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models


class Brand(models.Model):
    name = models.CharField(max_length=255, unique=True)

    class Meta:
        ordering = ['-id']


class Vehicle(models.Model):

    class Type(models.TextChoices):
        ECONOMY = 'economy', 'Economy'
        ESTATE = 'estate', 'Estate'
        LUXURY = 'luxury', 'Luxury'
        SUV = 'suv', 'SUV'
        CARGO = 'cargo', 'Cargo'

    class FuelType(models.TextChoices):
        PETROL = 'petrol', 'Petrol'
        DIESEL = 'diesel', 'Diesel'
        HYBRID = 'hybrid', 'Hybrid'
        ELECTRIC = 'electric', 'Electric'

    brand = models.ForeignKey(Brand, on_delete=models.CASCADE)
    model = models.CharField(max_length=255)
    type = models.CharField(max_length=16, choices=Type.choices)
    fuel_type = models.CharField(max_length=16, choices=FuelType.choices)
    seats = models.PositiveSmallIntegerField(default=4, validators=[
        MaxValueValidator(16),
        MinValueValidator(1)
    ])

    class Meta:
        ordering = ['-id']


class VehicleRent(models.Model):
    picture = models.TextField()
    price = models.FloatField()
    count = models.PositiveIntegerField()

    vehicle = models.ForeignKey(Vehicle, on_delete=models.CASCADE)

    class Meta:
        ordering = ['-id']


class RentalEvent(models.Model):
    start_date = models.DateTimeField(auto_now_add=True)
    end_date = models.DateTimeField(null=True, blank=True)

    user = models.ForeignKey('User', on_delete=models.CASCADE)
    vehicle_rent = models.ForeignKey(VehicleRent, on_delete=models.CASCADE)


class User(AbstractUser):
    phone_number = models.CharField(max_length=64, null=True, blank=True)
    money = models.IntegerField(default=0, blank=True)

    class Meta:
        ordering = ['-id']
