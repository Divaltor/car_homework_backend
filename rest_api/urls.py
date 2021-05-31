from django.urls import path, include
from rest_framework import routers

from rest_api.views import VehicleViewSet, UserViewSet, VehicleRentView, CurrentUserView, VehicleRentSet, \
    CurrentUserDiscountView, RentalEventSet, BrandViewSet

router = routers.DefaultRouter()
router.register(r'vehicles', VehicleViewSet)
router.register(r'users', UserViewSet)
router.register(r'vehicles-rent', VehicleRentSet)
router.register(r'rental-events', RentalEventSet)
router.register(r'brands', BrandViewSet)

urlpatterns = [
    path('', include(router.urls)),
    path('api/rent/<int:rent_id>', VehicleRentView.as_view()),
    path('api/users/current', CurrentUserView.as_view()),
    path('api/users/current/discount', CurrentUserDiscountView.as_view())
]
