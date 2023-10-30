from django.contrib import admin
from .models import Payment, Order, OrderedTokens, Meter, RoomMeterAssociation, Tenant

class OrderedTokenInline(admin.TabularInline):
    model = OrderedTokens
    readonly_fields = ('order', 'payment','user', 'quantity', 'price', 'amount')
    extra = 0

class OrderAdmin(admin.ModelAdmin):
    list_display =['order_number', 'name', 'phone', 'email', 'payment_method', 'status', 'is_ordered']
    inlines = [OrderedTokenInline]

admin.site.register(Payment)
admin.site.register(Order, OrderAdmin)
admin.site.register(OrderedTokens)
admin.site.register(Meter)
admin.site.register(RoomMeterAssociation)
admin.site.register(Tenant)
