# Generated by Django 4.2.6 on 2023-10-25 12:12

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = []

    operations = [
        migrations.CreateModel(
            name="Meter",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("meter_number", models.CharField(max_length=10)),
                ("current_value", models.DecimalField(decimal_places=2, max_digits=10)),
                (
                    "threshold_value",
                    models.DecimalField(decimal_places=2, max_digits=10),
                ),
            ],
        ),
        migrations.CreateModel(
            name="Tenant",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("room_number", models.CharField(max_length=10)),
                ("mobile_phone", models.CharField(max_length=15)),
                (
                    "meter",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE, to="api.meter"
                    ),
                ),
            ],
        ),
        migrations.CreateModel(
            name="Payment",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("amount_paid", models.DecimalField(decimal_places=2, max_digits=10)),
                ("payment_date", models.DateTimeField()),
                (
                    "tenant",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE, to="api.tenant"
                    ),
                ),
            ],
        ),
    ]