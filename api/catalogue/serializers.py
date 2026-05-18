from django.db import transaction
from rest_framework import serializers

from catalogue.models import (
    Artist,
    Price,
    PriceShow,
    Representation,
    RepresentationReservation,
    Reservation,
    Review,
    Show,
)

class ArtistSerializer(serializers.ModelSerializer):
    class Meta:
        model = Artist
        fields = ['id', 'firstname', 'lastname']


class PriceSerializer(serializers.ModelSerializer):
    class Meta:
        model = Price
        fields = ["id", "type", "price", "description"]


class RepresentationSerializer(serializers.ModelSerializer):
    show_title = serializers.CharField(source="show.title", read_only=True)
    location_name = serializers.CharField(source="location.designation", read_only=True)

    class Meta:
        model = Representation
        fields = ["id", "schedule", "show", "show_title", "location", "location_name"]


class ReviewSerializer(serializers.ModelSerializer):
    username = serializers.CharField(source="user.username", read_only=True)

    class Meta:
        model = Review
        fields = ["id", "username", "stars", "review", "created_at"]


class ShowSerializer(serializers.ModelSerializer):
    location_name = serializers.CharField(source="location.designation", read_only=True)
    prices = PriceSerializer(many=True, read_only=True)
    representations = RepresentationSerializer(many=True, read_only=True)
    reviews = serializers.SerializerMethodField()

    def get_reviews(self, obj):
        reviews = obj.reviews.filter(validated=True).select_related("user")
        return ReviewSerializer(reviews, many=True).data

    class Meta:
        model = Show
        fields = [
            "id",
            "slug",
            "title",
            "description",
            "poster_url",
            "duration",
            "created_in",
            "bookable",
            "location",
            "location_name",
            "prices",
            "representations",
            "reviews",
        ]


class ReviewCreateSerializer(serializers.Serializer):
    stars = serializers.IntegerField(min_value=1, max_value=5)
    review = serializers.CharField(max_length=2000)

    def create(self, validated_data):
        request = self.context["request"]
        show = self.context["show"]
        return Review.objects.create(
            user=request.user,
            show=show,
            stars=validated_data["stars"],
            review=validated_data["review"],
            validated=False,
        )


class ReservationItemSerializer(serializers.ModelSerializer):
    representation = RepresentationSerializer(read_only=True)
    line_total = serializers.DecimalField(max_digits=10, decimal_places=2, read_only=True)

    class Meta:
        model = RepresentationReservation
        fields = ["id", "representation", "price", "quantity", "line_total"]


class ReservationSerializer(serializers.ModelSerializer):
    status_label = serializers.CharField(source="get_status_display", read_only=True)
    total_amount = serializers.DecimalField(max_digits=10, decimal_places=2, read_only=True)
    items = ReservationItemSerializer(
        source="representation_reservations",
        many=True,
        read_only=True,
    )

    class Meta:
        model = Reservation
        fields = ["id", "booking_date", "status", "status_label", "total_amount", "items"]


class ReservationCreateSerializer(serializers.Serializer):
    representation_id = serializers.PrimaryKeyRelatedField(
        queryset=Representation.objects.select_related("show"),
        source="representation",
    )
    price_show_id = serializers.PrimaryKeyRelatedField(
        queryset=PriceShow.objects.select_related("price", "show"),
        source="price_show",
    )
    quantity = serializers.IntegerField(min_value=1, max_value=10)

    def validate(self, attrs):
        representation = attrs["representation"]
        price_show = attrs["price_show"]

        if not representation.show.bookable:
            raise serializers.ValidationError("Ce spectacle n'est pas reservable.")

        if price_show.show_id != representation.show_id:
            raise serializers.ValidationError("Ce tarif ne correspond pas au spectacle choisi.")

        return attrs

    def create(self, validated_data):
        request = self.context["request"]
        representation = validated_data["representation"]
        price_show = validated_data["price_show"]
        quantity = validated_data["quantity"]

        with transaction.atomic():
            reservation = Reservation.objects.create(
                user=request.user,
                status=Reservation.Status.CONFIRMED,
            )
            RepresentationReservation.objects.create(
                representation=representation,
                reservation=reservation,
                price=price_show.price.price,
                quantity=quantity,
            )

        return reservation
