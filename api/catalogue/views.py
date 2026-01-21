# from rest_framework.permissions import DjangoModelPermissions
from rest_framework import generics
from catalogue.models import Artist
from .serializers import ArtistSerializer
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
