# Generated by Django 4.2.6 on 2023-11-07 14:08

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("api", "0007_order_room_number_alter_order_order_number"),
    ]

    operations = [
        migrations.AlterField(
            model_name="order",
            name="order_number",
            field=models.CharField(default="1000199594", max_length=10),
        ),
    ]
