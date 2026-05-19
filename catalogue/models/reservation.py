from django.db import models
from django.contrib.auth.models import User


class Reservation(models.Model):
    class Status(models.TextChoices):
        PENDING = "pending", "En attente de paiement"
        CONFIRMED = "confirmed", "Confirmee"
        CANCELED = "canceled", "Annulee"

    class PaymentStatus(models.TextChoices):
        UNPAID = "unpaid", "Non paye"
        PAID = "paid", "Paye"
        FAILED = "failed", "Echoue"

    booking_date = models.DateTimeField(auto_now_add=True)
    status = models.CharField(
        max_length=60,
        choices=Status.choices,
        default=Status.CONFIRMED,
    )
    payment_status = models.CharField(
        max_length=30,
        choices=PaymentStatus.choices,
        default=PaymentStatus.PAID,
    )
    payment_method = models.CharField(max_length=30, blank=True)
    payment_provider = models.CharField(max_length=30, blank=True, default="stripe")
    payment_reference = models.CharField(max_length=255, blank=True)
    user = models.ForeignKey(
        User,
        on_delete=models.RESTRICT,
        null=False,
        related_name='reservations'
    )

    def __str__(self):
        return f"{self.user} - {self.booking_date}"

    @property
    def total_amount(self):
        return sum(item.line_total for item in self.representation_reservations.all())

    @property
    def is_cancelable(self):
        return self.status in {self.Status.PENDING, self.Status.CONFIRMED}

    @property
    def is_paid(self):
        return self.payment_status == self.PaymentStatus.PAID

    def mark_paid(self, payment_reference="", payment_method=""):
        self.status = self.Status.CONFIRMED
        self.payment_status = self.PaymentStatus.PAID
        self.payment_reference = payment_reference or self.payment_reference
        self.payment_method = payment_method or self.payment_method
        self.save(update_fields=["status", "payment_status", "payment_reference", "payment_method"])

    class Meta:
        db_table = "reservations"
