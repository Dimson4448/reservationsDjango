from rest_framework import generics, status
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from catalogue.models import Artist, Representation, Reservation, Show
from .serializers import (
    ArtistSerializer,
    RepresentationSerializer,
    ReservationCreateSerializer,
    ReservationSerializer,
    ShowSerializer,
)
from .permissions import IsAuthenticatedOrReadOnly


class ArtistListCreateView(generics.ListCreateAPIView):
    queryset = Artist.objects.all()
    serializer_class = ArtistSerializer
    # permission_classes = [DjangoModelPermissions]
    permission_classes = [IsAuthenticatedOrReadOnly]


class ArtistRetrieveUpdateDestroyView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Artist.objects.all()
    serializer_class = ArtistSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]


class ShowListView(generics.ListAPIView):
    queryset = (
        Show.objects
        .select_related("location")
        .prefetch_related("prices", "representations__show", "representations__location")
        .all()
    )
    serializer_class = ShowSerializer
    permission_classes = [AllowAny]


class ShowDetailView(generics.RetrieveAPIView):
    queryset = (
        Show.objects
        .select_related("location")
        .prefetch_related("prices", "representations__show", "representations__location")
        .all()
    )
    serializer_class = ShowSerializer
    permission_classes = [AllowAny]


class RepresentationListView(generics.ListAPIView):
    queryset = (
        Representation.objects
        .select_related("show", "location")
        .order_by("schedule")
    )
    serializer_class = RepresentationSerializer
    permission_classes = [AllowAny]


class ReservationListCreateView(generics.ListCreateAPIView):
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return (
            Reservation.objects
            .filter(user=self.request.user)
            .prefetch_related(
                "representation_reservations__representation__show",
                "representation_reservations__representation__location",
            )
            .order_by("-booking_date")
        )

    def get_serializer_class(self):
        if self.request.method == "POST":
            return ReservationCreateSerializer
        return ReservationSerializer

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        reservation = serializer.save()
        output = ReservationSerializer(reservation, context=self.get_serializer_context())
        return Response(output.data, status=status.HTTP_201_CREATED)


class ReservationCancelView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, pk):
        reservation = generics.get_object_or_404(
            Reservation.objects.filter(user=request.user),
            pk=pk,
        )
        reservation.status = Reservation.Status.CANCELED
        reservation.save(update_fields=["status"])
        return Response(ReservationSerializer(reservation).data)
