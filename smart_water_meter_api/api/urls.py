from django.urls import path
from .views import HomeView, register_tenant, esp_endpoint, room_meter_association, enter_meter_number
from . import views
urlpatterns = [
    path('', HomeView.as_view(), name='home'),
    path('register/', register_tenant, name='register'),
    path('esp/', esp_endpoint, name='esp'),
    path('room_meter_association/', room_meter_association, name='room_meter_association'),
    path('enter_meter_number/', enter_meter_number, name='enter_meter_number'),
    path('place_order/', views.place_order, name='place_order'),
    path('payments/', views.payments, name='payments'),
    # path('confirm_payment/<int:order_id>/', views.confirm_payment, name='confirm_payment'),
    path('order_complete', views.order_complete, name='order_complete'),
    path('confirm_order/', views.confirm_order, name='confirm_order'),
    path('success/', views.success_view, name='success'),
]

