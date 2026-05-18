from django.db import models
from django.contrib.auth.models import User


class Reservation(models.Model):
    class Status(models.TextChoices):
        CONFIRMED = "confirmed", "Confirmee"
        CANCELED = "canceled", "Annulee"

    booking_date = models.DateTimeField(auto_now_add=True)
    status = models.CharField(
        max_length=60,
        choices=Status.choices,
        default=Status.CONFIRMED,
    )
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
        return self.status == self.Status.CONFIRMED

    class Meta:
        db_table = "reservations"
