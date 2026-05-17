from django import forms

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
    )

    def __init__(self, *args, representation=None, **kwargs):
        super().__init__(*args, **kwargs)
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
