from django.urls import path
from .views import HomeView, register_tenant, make_payment, esp_endpoint, room_meter_association, enter_meter_number

urlpatterns = [
    path('', HomeView.as_view(), name='home'),
    path('register/', register_tenant, name='register'),
    path('payment/', make_payment, name='payment'),
    path('esp/', esp_endpoint, name='esp'),
    path('room_meter_association/', room_meter_association, name='room_meter_association'),
    path('enter_meter_number/', enter_meter_number, name='enter_meter_number'),
]
