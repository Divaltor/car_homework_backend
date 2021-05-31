import random

from django.core.management import BaseCommand
from django_seed import Seed
from django_seed.seeder import Seeder
from faker import Faker
from faker_vehicle import VehicleProvider

from rest_api.models import Brand, Vehicle, VehicleRent, User


class Command(BaseCommand):
    def __init__(self, stdout=None, stderr=None, no_color=False, force_color=False):
        super().__init__(stdout, stderr, no_color, force_color)
        self._seeder: Seeder = Seed.seeder()
        self._faker: Faker = self._seeder.faker
        self._faker.add_provider(VehicleProvider)

    def handle(self, *args, **options):
        self._seed_brands()
        self._seed_vehicles()
        self._seed_vehicles_rent()

        users = [('admin', 'admin@admin.com'), ('test', 'test@test.com'), ('user', 'user@user.com')]

        for user in users:
            username, password = user

            created_user = User.objects.create_user(username=username, password='admin', email=password, money=self._faker.pyint(min_value=10_000, max_value=100_000))

        self.stdout.write(self.style.SUCCESS('Seeding is completed'))

    def _seed_vehicles_rent(self):
        rents = [
            VehicleRent(
                picture=self._faker.image_url(),
                price=round(self._faker.pyfloat(min_value=50, max_value=5000), 2),
                count=self._faker.pyint(min_value=0, max_value=50),
                vehicle_id=Vehicle.objects.order_by('?')[0].id
            )
            for _ in range(500)
        ]

        VehicleRent.objects.bulk_create(rents)

    def _seed_vehicles(self):
        vehicles = [self._faker.vehicle_object() for _ in range(1500)]

        vehicle_types = {
            'SUV': Vehicle.Type.SUV,
            'Pickup': Vehicle.Type.ECONOMY,
            'Sedan': Vehicle.Type.ECONOMY,
            'Convertible': Vehicle.Type.LUXURY,
            'Van/Minivan': Vehicle.Type.SUV,
            'Hatchback': Vehicle.Type.LUXURY,
            'Coupe': Vehicle.Type.LUXURY,
            'Wagon': Vehicle.Type.CARGO
        }

        unique_vehicles = []

        [unique_vehicles.append(vehicle) for vehicle in vehicles if vehicle['Model'] not in unique_vehicles]

        vehicle_objs = []

        for vehicle in unique_vehicles:
            type = vehicle['Category'].split(', ')[0]

            if type not in vehicle_types:
                continue

            try:
                brand = Brand.objects.get(name=vehicle['Make'])
            except Brand.DoesNotExist:
                continue

            vehicle_objs.append(Vehicle(model=vehicle['Model'], type=vehicle_types[type],
                                        fuel_type=random.choice(Vehicle.FuelType.labels), brand_id=brand.id,
                                        seats=random.randint(1, 6)))

        Vehicle.objects.bulk_create(vehicle_objs)

    def _seed_brands(self):
        brands = list(set([self._faker.vehicle_make() for _ in range(100)]))

        Brand.objects.bulk_create([Brand(name=brand) for brand in brands])
