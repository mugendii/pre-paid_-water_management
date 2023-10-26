from django import forms
from .models import Tenant, RoomMeterAssociation, Meter

class TenantRegistrationForm(forms.Form):
    room_number = forms.CharField(max_length=10)
    mobile_phone = forms.CharField(max_length=15)

class PaymentForm(forms.Form):
    tenant = forms.ModelChoiceField(queryset=Tenant.objects.all())
    amount_paid = forms.DecimalField(max_digits=10, decimal_places=2)


class RoomMeterAssociationForm(forms.ModelForm):
    class Meta:
        model = RoomMeterAssociation
        fields = ['room_number', 'meter']

class MeterForm(forms.ModelForm):
    class Meta:
        model = Meter
        fields = ['meter_number', 'current_value', 'threshold_value']

