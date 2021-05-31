from rest_framework import serializers

from rest_api.models import Vehicle, User, VehicleRent, RentalEvent, Brand


class BrandSerializer(serializers.ModelSerializer):

    class Meta:
        model = Brand
        fields = '__all__'


class VehicleSerializer(serializers.ModelSerializer):
    brand = serializers.SlugRelatedField(read_only=True, slug_field='name')

    class Meta:
        model = Vehicle
        fields = '__all__'


class UserSerializer(serializers.ModelSerializer):

    class Meta:
        model = User
        fields = ['id', 'username', 'first_name', 'last_name', 'email', 'phone_number', 'money']


class VehicleRentSerializer(serializers.ModelSerializer):
    vehicle = VehicleSerializer(read_only=True)

    class Meta:
        model = VehicleRent
        fields = '__all__'


class RentalEventSerializer(serializers.ModelSerializer):

    vehicle = VehicleRentSerializer(read_only=True)

    class Meta:
        model = RentalEvent
        fields = '__all__'
