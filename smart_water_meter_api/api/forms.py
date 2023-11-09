from django import forms
from .models import Tenant, RoomMeterAssociation, Meter, Order

class TenantRegistrationForm(forms.Form):
    room_number = forms.CharField(max_length=10)
    mobile_phone = forms.CharField(max_length=15)

class OrderForm(forms.ModelForm):
    class Meta:
        model = Order
        fields = ['first_name', 'last_name', 'phone','room_number', 'email', 'city', 'total']
        
        widgets = {
            'first_name': forms.TextInput(attrs={'class': 'h-10 border mt-1 rounded px-4 w-full bg-gray-50'}),
            'last_name': forms.TextInput(attrs={'class': 'h-10 border mt-1 rounded px-4 w-full bg-gray-50'}),
            'phone': forms.TextInput(attrs={'class': 'h-10 border mt-1 rounded px-4 w-full bg-gray-50'}),
            'room_number': forms.TextInput(attrs={'class': 'h-10 border mt-1 rounded px-4 w-full bg-gray-50'}), # 'readonly': 'readonly
            'email': forms.TextInput(attrs={'class': 'h-10 border mt-1 rounded px-4 w-full bg-gray-50'}),
            'city': forms.TextInput(attrs={'class': 'h-10 border mt-1 rounded px-4 w-full bg-gray-50'}),
            'total': forms.TextInput(attrs={'class': 'h-10 border mt-1 rounded px-4 w-full bg-gray-50'}),
        }

class RoomMeterAssociationForm(forms.ModelForm):
    class Meta:
        model = RoomMeterAssociation
        fields = ['room_number', 'meter']

class MeterForm(forms.ModelForm):
    class Meta:
        model = Meter
        fields = ['meter_number', 'current_value', 'threshold_value']

