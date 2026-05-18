from django import forms

from catalogue.models import Review


class ReviewForm(forms.ModelForm):
    class Meta:
        model = Review
        fields = ["stars", "review"]
        labels = {
            "stars": "Note",
            "review": "Votre avis",
        }
        widgets = {
            "stars": forms.NumberInput(attrs={"min": 1, "max": 5}),
            "review": forms.Textarea(attrs={"rows": 4}),
        }

    def clean_stars(self):
        stars = self.cleaned_data["stars"]
        if stars < 1 or stars > 5:
            raise forms.ValidationError("La note doit etre comprise entre 1 et 5.")
        return stars
