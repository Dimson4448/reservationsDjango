from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.contrib.auth.models import User

from catalogue.models import (
    Artist,
    ArtistType,
    ArtistTypeShow,
    Locality,
    Location,
    Price,
    PriceShow,
    Representation,
    RepresentationReservation,
    Reservation,
    Review,
    Show,
    Type,
    UserMeta,
)


class UserMetaInline(admin.StackedInline):
    model = UserMeta
    can_delete = False
    verbose_name_plural = "Profil"


class UserAdmin(BaseUserAdmin):
    inlines = [UserMetaInline]


for model in [
    Artist,
    ArtistType,
    ArtistTypeShow,
    Locality,
    Location,
    Price,
    PriceShow,
    Representation,
    RepresentationReservation,
    Reservation,
    Review,
    Show,
    Type,
]:
    admin.site.register(model)


admin.site.unregister(User)
admin.site.register(User, UserAdmin)
