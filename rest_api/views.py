from datetime import timedelta, datetime
from http import HTTPStatus

from dateutil.parser import isoparse
from django.utils.timezone import now
from rest_framework import viewsets, generics
from rest_framework.pagination import PageNumberPagination
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from rest_framework_simplejwt.views import TokenObtainPairView

from rest_api.models import Vehicle, User, VehicleRent, RentalEvent, Brand
from rest_api.serializers import VehicleSerializer, UserSerializer, VehicleRentSerializer, RentalEventSerializer, \
    BrandSerializer


class Discount:

    def __init__(self, days: int):
        self.days = days

    @property
    def discount(self) -> int:
        if self.days > 10:
            return 10
        elif self.days > 5:
            return 7
        elif self.days > 3:
            return 5

        return 0


class Unpaginatable(PageNumberPagination):
    def paginate_queryset(self, queryset, request, view=None):
        if request.query_params.get('get_all', False) == 'true':
            return None

        return super(PageNumberPagination, self).paginate_queryset(queryset, request, view=view)


class BrandViewSet(viewsets.ModelViewSet):
    queryset = Brand.objects.all()
    serializer_class = BrandSerializer
    pagination_class = Unpaginatable


class VehicleViewSet(viewsets.ModelViewSet):
    queryset = Vehicle.objects.all()
    serializer_class = VehicleSerializer


class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer


class VehicleRentSet(viewsets.ModelViewSet):
    queryset = VehicleRent.objects.all()
    serializer_class = VehicleRentSerializer


class RentalEventSet(viewsets.ModelViewSet):
    serializer_class = RentalEventSerializer
    queryset = RentalEvent.objects.all()
    filterset_fields = ['user_id']
    pagination_class = Unpaginatable


class CurrentUserView(APIView):

    def get(self, request: Request, *args, **kwargs):
        user = User.objects.get(pk=request.user.id)

        return Response(UserSerializer(user).data)


class VehicleRentView(APIView):

    def post(self, request: Request, rent_id: int, *args, **kwargs):

        start = isoparse(request.data['start'])
        end = isoparse(request.data['end'])

        diff = (end - start) + timedelta(days=1)

        events = RentalEvent.objects.filter(user_id=request.user.id,
                                            start_date__gte=now() - timedelta(days=60)).count()

        if events >= 3:
            discount = 15
        else:
            discount = Discount(diff.days).discount

        try:
            vehicle = VehicleRent.objects.get(pk=rent_id)
        except VehicleRent.DoesNotExist:
            return Response(status=HTTPStatus.BAD_REQUEST)

        end_price = vehicle.price - (vehicle.price * (discount / 100))

        if end_price > request.user.money:
            return Response({
                'detail': 'Not enough money'
            }, status=HTTPStatus.FORBIDDEN)

        request.user.money = request.user.money - end_price
        request.user.save()

        vehicle.count = vehicle.count - 1
        vehicle.save()

        event = RentalEvent(start_date=start, end_date=end, user_id=request.user.id, vehicle_rent=vehicle)
        event.save()

        event = VehicleRentSerializer(event.vehicle_rent).data
        event.update({'balance': request.user.money})

        return Response(event, status=HTTPStatus.OK)


class CurrentUserDiscountView(APIView):

    def get(self, request: Request, *args, **kwargs):
        date_before = datetime.today() - timedelta(days=60)

        events = RentalEvent.objects.filter(user_id=request.user.id, start_date__gte=date_before).count()

        return Response({
            'discount': True if events >= 3 else False
        })


class JwtTokenSerializer(TokenObtainPairSerializer):

    @classmethod
    def get_token(cls, user):
        token = super().get_token(user)

        token['username'] = user.username
        token['admin'] = user.is_superuser

        return token


class JwtTokenView(TokenObtainPairView):
    serializer_class = JwtTokenSerializer
