from django import forms
from django.core.exceptions import ValidationError

from catalogue.models import PriceShow, Representation


class ReservationForm(forms.Form):
    representation = forms.ModelChoiceField(
        queryset=Representation.objects.none(),
        widget=forms.HiddenInput,
    )
    price_show = forms.ModelChoiceField(
        queryset=PriceShow.objects.none(),
        label="Tarif",
    )
    quantity = forms.IntegerField(
        label="Nombre de places",
        min_value=1,
        max_value=10,
        initial=1,
        help_text="Vous pouvez reserver entre 1 et 10 places par commande.",
        error_messages={
            "min_value": "Vous devez reserver au moins une place.",
            "max_value": "Vous ne pouvez pas reserver plus de 10 places en une commande.",
            "invalid": "Le nombre de places doit etre un nombre entier.",
        },
    )

    def __init__(self, *args, representation=None, **kwargs):
        super().__init__(*args, **kwargs)
        self.representation = representation
        if representation is not None:
            self.fields["representation"].queryset = Representation.objects.filter(pk=representation.pk)
            self.fields["representation"].initial = representation
            self.fields["price_show"].queryset = (
                PriceShow.objects
                .filter(show=representation.show)
                .select_related("price")
                .order_by("price__price")
            )
        self.fields["price_show"].label_from_instance = (
            lambda price_show: f"{price_show.price.type} - {price_show.price.price} EUR"
        )

    def clean(self):
        cleaned_data = super().clean()
        representation = cleaned_data.get("representation")
        price_show = cleaned_data.get("price_show")

        if self.representation and representation != self.representation:
            raise ValidationError("Representation invalide.")

        if self.representation and price_show and price_show.show_id != self.representation.show_id:
            raise ValidationError("Ce tarif ne correspond pas au spectacle choisi.")

        return cleaned_data
