from django.db import models

class Tenant(models.Model):
    room_number = models.CharField(max_length=10)
    mobile_phone = models.CharField(max_length=15)

class Meter(models.Model):
    meter_number = models.CharField(max_length=10)
    current_value = models.DecimalField(max_digits=10, decimal_places=2)
    threshold_value = models.DecimalField(max_digits=10, decimal_places=2)

class Payment(models.Model):
    tenant = models.ForeignKey('Tenant', on_delete=models.CASCADE)
    amount_paid = models.DecimalField(max_digits=10, decimal_places=2)
    payment_date = models.DateTimeField()

class RoomMeterAssociation(models.Model):
    room_number = models.CharField(max_length=10)
    meter = models.ForeignKey(Meter, on_delete=models.CASCADE)
