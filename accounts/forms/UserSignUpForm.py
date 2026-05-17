from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import Group, User
from django.db import models

from catalogue.models import UserMeta


class UserSignUpForm(UserCreationForm):
    class Language(models.TextChoices):
        FRENCH = "fr", "Francais"
        ENGLISH = "en", "English"
        DUTCH = "nl", "Nederlands"

    username = forms.CharField(max_length=30, label="Login")
    first_name = forms.CharField(max_length=60, label="Prenom")
    last_name = forms.CharField(max_length=60, label="Nom")
    email = forms.EmailField(label="Email")
    langue = forms.ChoiceField(choices=Language.choices, label="Langue")

    class Meta:
        model = User
        fields = [
            "username",
            "email",
            "password1",
            "password2",
            "first_name",
            "last_name",
            "langue",
        ]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["password1"].label = "Mot de passe"
        self.fields["password2"].label = "Confirmation du mot de passe"
        for field_name in ["username", "password1", "password2"]:
            self.fields[field_name].help_text = None

    def save(self, commit=True):
        user = super().save(commit=False)
        if commit:
            user.save()
            member_group, _created = Group.objects.get_or_create(name="MEMBER")
            member_group.user_set.add(user)
            UserMeta.objects.update_or_create(
                user=user,
                defaults={"langue": self.cleaned_data["langue"]},
            )
        return user
