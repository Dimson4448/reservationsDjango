from django.db import migrations, models


def mark_existing_confirmed_reservations_paid(apps, schema_editor):
    Reservation = apps.get_model("catalogue", "Reservation")
    Reservation.objects.filter(
        status="confirmed",
        payment_status="unpaid",
    ).update(payment_status="paid")


class Migration(migrations.Migration):

    dependencies = [
        ("catalogue", "0019_reservation_payment_method_and_more"),
    ]

    operations = [
        migrations.RunPython(mark_existing_confirmed_reservations_paid, migrations.RunPython.noop),
        migrations.AlterField(
            model_name="reservation",
            name="payment_status",
            field=models.CharField(
                choices=[("unpaid", "Non paye"), ("paid", "Paye"), ("failed", "Echoue")],
                default="paid",
                max_length=30,
            ),
        ),
    ]
