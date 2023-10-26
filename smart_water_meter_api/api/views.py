from django.shortcuts import render, redirect
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from rest_framework.response import Response
from rest_framework.decorators import api_view
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.views.generic import TemplateView

from .models import Payment, RoomMeterAssociation, Meter, Tenant
from .forms import TenantRegistrationForm, PaymentForm, RoomMeterAssociationForm, Tenant, MeterForm


class HomeView(TemplateView):
    template_name = 'api/home.html'


def register_tenant(request):
    if request.method == 'POST':
        form = TenantRegistrationForm(request.POST)
        if form.is_valid():
            # Create a new tenant
            room_number = form.cleaned_data['room_number']
            mobile_phone = form.cleaned_data['mobile_phone']
            # Find the association between room number and meter
            try:
                association = RoomMeterAssociation.objects.get(room_number=room_number)
                meter = association.meter
            except RoomMeterAssociation.DoesNotExist:
                # Handle the case where no association is found
                # You can redirect to an error page or show an error message
                return render(request, 'api/error.html', {'error_message': 'No association found for this room number.'})

            # Create a new tenant instance and associate it with the meter
            tenant = Tenant(room_number=room_number, mobile_phone=mobile_phone, meter=meter)
            tenant.save()

            return redirect('payment')

    else:
        form = TenantRegistrationForm()

    return render(request, 'api/register_tenant.html', {'form': form})

def make_payment(request):
    if request.method == 'POST':
        form = PaymentForm(request.POST)
        if form.is_valid():
            # Handle the payment and solenoid valve control here
            payment = form.save()
            # Update meter values, send signals to ESP, etc.
            return redirect('home')

    else:
        form = PaymentForm()

    return render(request, 'api/make_payment.html', {'form': form})



@csrf_exempt
def esp_endpoint(request):
    if request.method == 'POST':
        # Handle data from the ESP and control solenoid valve
        data = request.POST
        # Compare values and control the solenoid valve

    # Return a response to the ESP
    response_data = {"message": "Data received and processed"}
    return JsonResponse(response_data)


@receiver(post_save, sender=Payment)
def handle_payment(sender, instance, **kwargs):
    # Handle actions when a payment is made
    # Update the meter value and send signals to the ESP
    pass




def room_meter_association(request):
    if request.method == 'POST':
        form = RoomMeterAssociationForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('success')  # Redirect to a success page or another appropriate page

    else:
        form = RoomMeterAssociationForm()

    return render(request, 'api/room_meter_association.html', {'form': form})

def enter_meter_number(request):
    if request.method == 'POST':
        form = MeterForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('home') 

    else:
        form = MeterForm()

    return render(request, 'api/enter_meter_number.html', {'form': form})
