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


@admin.register(Artist)
class ArtistAdmin(admin.ModelAdmin):
    list_display = ("lastname", "firstname")
    search_fields = ("lastname", "firstname")
    ordering = ("lastname", "firstname")


@admin.register(Show)
class ShowAdmin(admin.ModelAdmin):
    list_display = ("title", "location", "bookable", "created_in", "representation_count")
    list_filter = ("bookable", "created_in", "location")
    search_fields = ("title", "description", "location__designation")
    autocomplete_fields = ("location",)
    list_editable = ("bookable",)
    list_select_related = ("location",)
    ordering = ("title",)

    @admin.display(description="Representations")
    def representation_count(self, obj):
        return obj.representations.count()


@admin.register(Representation)
class RepresentationAdmin(admin.ModelAdmin):
    list_display = ("show", "schedule", "location")
    list_filter = ("show", "location")
    search_fields = ("show__title", "location__designation")
    autocomplete_fields = ("show", "location")
    list_select_related = ("show", "location")
    date_hierarchy = "schedule"
    ordering = ("schedule",)


class RepresentationReservationInline(admin.TabularInline):
    model = RepresentationReservation
    extra = 0
    autocomplete_fields = ("representation",)
    readonly_fields = ("line_total",)


@admin.register(Reservation)
class ReservationAdmin(admin.ModelAdmin):
    list_display = ("id", "user", "booking_date", "status", "payment_status", "payment_method", "reserved_places", "total_amount")
    list_filter = ("status", "payment_status", "payment_method", "booking_date")
    search_fields = ("user__username", "user__email", "payment_reference")
    autocomplete_fields = ("user",)
    list_select_related = ("user",)
    readonly_fields = ("booking_date", "total_amount")
    date_hierarchy = "booking_date"
    inlines = [RepresentationReservationInline]
    actions = ["mark_confirmed", "mark_canceled"]

    @admin.display(description="Places")
    def reserved_places(self, obj):
        return sum(item.quantity for item in obj.representation_reservations.all())

    @admin.action(description="Marquer comme confirmees")
    def mark_confirmed(self, request, queryset):
        queryset.update(status=Reservation.Status.CONFIRMED)

    @admin.action(description="Marquer comme annulees")
    def mark_canceled(self, request, queryset):
        queryset.update(status=Reservation.Status.CANCELED)


@admin.register(Review)
class ReviewAdmin(admin.ModelAdmin):
    list_display = ("show", "user", "stars", "validated", "created_at")
    list_filter = ("validated", "stars", "created_at")
    search_fields = ("show__title", "user__username", "review")
    autocomplete_fields = ("show", "user")
    list_select_related = ("show", "user")
    readonly_fields = ("created_at", "updated_at")
    date_hierarchy = "created_at"
    list_editable = ("validated",)
    actions = ["validate_reviews", "unvalidate_reviews"]

    @admin.action(description="Valider les avis selectionnes")
    def validate_reviews(self, request, queryset):
        queryset.update(validated=True)

    @admin.action(description="Retirer la validation des avis selectionnes")
    def unvalidate_reviews(self, request, queryset):
        queryset.update(validated=False)


@admin.register(Location)
class LocationAdmin(admin.ModelAdmin):
    list_display = ("designation", "locality", "phone", "website")
    list_filter = ("locality",)
    search_fields = ("designation", "address", "locality__locality", "website", "phone")
    autocomplete_fields = ("locality",)
    list_select_related = ("locality",)
    ordering = ("designation",)


@admin.register(Price)
class PriceAdmin(admin.ModelAdmin):
    list_display = ("type", "price", "start_date", "end_date")
    list_filter = ("start_date", "end_date")
    search_fields = ("type", "description")
    ordering = ("price", "type")


@admin.register(PriceShow)
class PriceShowAdmin(admin.ModelAdmin):
    list_display = ("show", "price", "price_amount")
    list_filter = ("show", "price")
    search_fields = ("show__title", "price__type")
    autocomplete_fields = ("show", "price")
    list_select_related = ("show", "price")
    ordering = ("show__title", "price__price")

    @admin.display(description="Montant")
    def price_amount(self, obj):
        return obj.price.price


@admin.register(Locality)
class LocalityAdmin(admin.ModelAdmin):
    list_display = ("postal_code", "locality")
    search_fields = ("postal_code", "locality")
    ordering = ("postal_code", "locality")


for model in [
    ArtistType,
    ArtistTypeShow,
    RepresentationReservation,
    Type,
]:
    admin.site.register(model)


admin.site.unregister(User)
admin.site.register(User, UserAdmin)
