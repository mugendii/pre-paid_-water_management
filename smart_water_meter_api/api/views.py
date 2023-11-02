from django.shortcuts import render, redirect
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from rest_framework.response import Response
from rest_framework.decorators import api_view
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.views.generic import TemplateView
from django.shortcuts import render
from django.shortcuts import redirect
import simplejson as json
from .utils import generate_order_number, check_callback
from django.http import HttpResponse
import requests
import time
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from .models import Payment, RoomMeterAssociation, Meter, Tenant, Order, Payment, OrderedTokens
from .forms import TenantRegistrationForm, RoomMeterAssociationForm, Tenant, MeterForm, OrderForm


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



def place_order(request):
    if request.method == 'POST':
        form = OrderForm(request.POST)
        if form.is_valid():
            # Create an Order object with the form data
            order = form.save()
            return render(request, 'api/confirm_order.html', {'order': order})
    else:
        form = OrderForm()
    return render(request, 'api/place_order.html', {'form': form})

def confirm_order(request):
    if request.method == 'POST' and 'pay_now' in request.POST:
        # Get the order ID from the form data
        order_id = request.POST.get('order_id')

        # Retrieve the Order object based on the ID
        order = Order.objects.get(id=order_id)

        # For simplicity, you can assume the payment is successful
        # and update the order status
        order.status = 'Success'
        order.save()

        # Redirect to a thank you page or any other relevant page
        return redirect('home')

    return render(request, 'api/confirm_order.html')

def payments(request):
        # check if request is ajax or not
        if request.headers.get('x-requested-with') == 'XMLHttpRequest':
            # get the payment method
            order_number = request.POST.get('order_number')
            transaction_id = request.POST.get('transaction_id')
            payment_method = request.POST.get('payment_method')
            quantity = request.POST.get('quantity')
            price = request.POST.get('price')
            status = request.POST.get('status')
            print(order_number, transaction_id, payment_method, status)
            
            order = Order.objects.get(order_number=order_number, user=request.user)
            
            payment = Payment(
                user = request.user,
                transaction_id = transaction_id,
                payment_method = payment_method,
                amount = order.total,
                status = status   
            )
            payment.save()
            
            order.payment = payment
            order.is_ordered = True
            order.save()
            
            # TODO add metre number association with room here
            # room_number = Cart.objects.filter(user=request.user)
            
        
            ordered_tokens = OrderedTokens()
            ordered_tokens.order = order
            ordered_tokens.payment = payment
            ordered_tokens.user = request.user
        
            ordered_tokens.quantity = quantity
            ordered_tokens.price = price
            ordered_tokens.amount = price * quantity
            ordered_tokens.save()
        
            

            response ={
                'order_number': order.order_number,
                'transaction_id': transaction_id,
            }
            
            return JsonResponse(response)
        

        return HttpResponse('payment successful')
    
def order_complete(request):
    order_number = request.GET.get('order_no')
    transaction_id = request.GET.get('trans_id')
    
    try:
        order = Order.objects.get(order_number=order_number, payment__transaction_id=transaction_id, is_ordered=True)
        ordered_tokens = OrderedTokens.objects.filter(order=order)
        subtotal = 0
        for item in ordered_tokens:
            subtotal += item.price * item.quantity
        context={
            'order': order,
            'ordered_food': ordered_tokens,
            'to_email': order.email,
        }
        return render(request, 'api/order_complete.html',context)
    except:
        return redirect('api/home.html')
    return render(request, 'api/order_complete.html')