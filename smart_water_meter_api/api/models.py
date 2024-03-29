from django.db import models
from django.contrib.auth.models import User
import random

class Tenant(models.Model):
    room_number = models.CharField(max_length=10)
    mobile_phone = models.CharField(max_length=15)

class Meter(models.Model):
    meter_number = models.CharField(max_length=10)
    current_value = models.DecimalField(max_digits=10, decimal_places=2)
    threshold_value = models.DecimalField(max_digits=10, decimal_places=2)


class RoomMeterAssociation(models.Model):
    room_number = models.CharField(max_length=10)
    meter = models.ForeignKey(Meter, on_delete=models.CASCADE)


class Payment(models.Model):
    PAYMENT_METHOD = (
        ('PayPal', 'PayPal'),
        ('Mpesa', 'Mpesa'),
    )
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    transaction_id = models.CharField(max_length=100)
    payment_method = models.CharField(choices=PAYMENT_METHOD, max_length=100, default='Mpesa')
    amount = models.CharField(max_length=10)
    status = models.CharField(max_length=100)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.transaction_id



class Order(models.Model):
    STATUS = (
        ('Success', 'Success'),
        ('Pending', 'Pending'),
        ('Failed', 'Failed'),
        ('Cancelled', 'Cancelled'),
        ('Refunded', 'Refunded'),
    )

    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    payment = models.ForeignKey(Payment, on_delete=models.SET_NULL, blank=True, null=True)
    order_number = models.CharField(max_length=10, default=f'100{random.randint(100000, 999999)}')
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    phone = models.CharField(max_length=15, blank=True)
    room_number = models.CharField(max_length=10)
    email = models.EmailField(max_length=50)
    city = models.CharField(max_length=50)
    total = models.FloatField()
    payment_method = models.CharField(max_length=25)
    status = models.CharField(max_length=15, choices=STATUS, default='New')
    is_ordered = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    @property
    def name(self):
        return f'{self.first_name} {self.last_name}'

    def save(self, *args, **kwargs):
        if not self.order_number:
            # Generate a unique order number for each order
            while True:
                order_number = random.randint(100000, 999999)
                if not Order.objects.filter(order_number=order_number).exists():
                    self.order_number = order_number
                    break
        super(Order, self).save(*args, **kwargs)

    def __str__(self):
        return self.order_number


class OrderedTokens(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE)
    payment = models.ForeignKey(Payment, on_delete=models.SET_NULL, blank=True, null=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    quantity = models.IntegerField()
    price = models.FloatField()
    amount = models.FloatField()
    order_number = models.CharField(max_length=100)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)


    def __str__(self):
        return self.amount