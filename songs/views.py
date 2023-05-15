from django.shortcuts import get_object_or_404
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework.permissions import IsAuthenticatedOrReadOnly
from rest_framework.pagination import PageNumberPagination
from .serializers import SongSerializer
from albums.models import Album
from rest_framework import generics


class SongView(generics.ListCreateAPIView, PageNumberPagination):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticatedOrReadOnly]

    serializer_class = SongSerializer
    lookup_url_kwarg = "pk"
    pagination_class = PageNumberPagination
    paginate_by = 1

    def get_album(self) -> Album:
        album = album = get_object_or_404(Album, pk=self.kwargs["pk"])
        return album

    def get_queryset(self):
        album = self.get_album()
        queryset = album.songs.all()
        return queryset

    def perform_create(self, serializer) -> None:
        album = self.get_album()
        serializer.save(album=album)
