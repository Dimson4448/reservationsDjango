from django import forms
from django.contrib.auth.forms import UserChangeForm
from django.contrib.auth.models import User
from django.db import models

from catalogue.models import UserMeta


class UserUpdateForm(UserChangeForm):
    class Language(models.TextChoices):
        FRENCH = "fr", "Francais"
        ENGLISH = "en", "English"
        DUTCH = "nl", "Nederlands"

    username = forms.CharField(max_length=30, label="Login")
    first_name = forms.CharField(max_length=60, label="Prenom")
    last_name = forms.CharField(max_length=60, label="Nom")
    email = forms.EmailField(label="Email")
    password = None
    langue = forms.ChoiceField(choices=Language.choices, label="Langue")

    class Meta:
        model = User
        fields = [
            "username",
            "email",
            "first_name",
            "last_name",
            "langue",
        ]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["username"].help_text = None
        user = kwargs.get("instance")
        if user is not None:
            user_meta, _created = UserMeta.objects.get_or_create(
                user=user,
                defaults={"langue": "fr"},
            )
            self.initial["langue"] = user_meta.langue

    def save(self, commit=True):
        user = super().save(commit=False)
        if commit:
            user.save()
            UserMeta.objects.update_or_create(
                user=user,
                defaults={"langue": self.cleaned_data["langue"]},
            )
        return user
