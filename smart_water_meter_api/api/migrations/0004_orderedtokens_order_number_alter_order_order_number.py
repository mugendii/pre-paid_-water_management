# Generated by Django 4.2.6 on 2023-11-02 08:11

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("api", "0003_order_remove_meter_tenant_remove_payment_amount_paid_and_more"),
    ]

    operations = [
        migrations.AddField(
            model_name="orderedtokens",
            name="order_number",
            field=models.CharField(default=1000, max_length=100),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name="order",
            name="order_number",
            field=models.IntegerField(default=1000),
        ),
    ]
