from django.contrib import messages
from django.contrib.auth import logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import UserPassesTestMixin
from django.contrib.auth.models import User
from django.shortcuts import get_object_or_404, redirect, render
from django.urls import reverse_lazy
from django.views.generic.edit import CreateView, UpdateView

from .forms import UserSignUpForm, UserUpdateForm
from catalogue.models import UserMeta


class UserUpdateView(UserPassesTestMixin, UpdateView):
    model = User
    form_class = UserUpdateForm
    success_url = reverse_lazy("accounts:user-profile")
    template_name = "user/update.html"

    def test_func(self):
        pk_in_url = self.kwargs["pk"]
        return (
            self.request.user.is_authenticated
            and (self.request.user.id == pk_in_url or self.request.user.is_superuser)
        )

    def handle_no_permission(self):
        messages.error(self.request, "Vous n'avez pas l'autorisation d'acceder a cette page.")
        return redirect("accounts:user-profile")


class UserSignUpView(UserPassesTestMixin, CreateView):
    form_class = UserSignUpForm
    success_url = reverse_lazy("login")
    template_name = "registration/signup.html"

    def test_func(self):
        return self.request.user.is_anonymous or self.request.user.is_superuser

    def handle_no_permission(self):
        messages.error(self.request, "Vous etes deja inscrit.")
        return redirect("home")


@login_required
def profile(request):
    languages = {
        "fr": "Francais",
        "en": "English",
        "nl": "Nederlands",
    }
    user_meta, _created = UserMeta.objects.get_or_create(
        user=request.user,
        defaults={"langue": "fr"},
    )
    reservations = (
        request.user.reservations
        .prefetch_related("representation_reservations__representation__show")
        .order_by("-booking_date")
    )

    return render(request, "user/profile.html", {
        "user_language": languages.get(user_meta.langue, user_meta.langue),
        "reservations": reservations,
    })


@login_required
def delete(request, pk):
    if request.method != "POST" or request.POST.get("_method", "").upper() != "DELETE":
        messages.error(request, "Suppression interdite.")
        return redirect("accounts:user-profile")

    user = get_object_or_404(User, id=pk)
    if request.user.id != user.id and not request.user.is_superuser:
        messages.error(request, "Suppression d'un autre compte interdite.")
        return redirect("accounts:user-profile")

    user.delete()
    logout(request)
    messages.success(request, "Utilisateur supprime avec succes.")
    return redirect("home")
