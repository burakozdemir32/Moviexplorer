from django.shortcuts import render
from .models import Movie, MovieRatings, MovieActorIndex, MovieDirectorIndex, Person
from .serializers import MovieSerializer

from rest_framework import viewsets


class MovieViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Movie.objects.filter(genres__contains=['Horror', 'Thriller', 'Comedy'])
    serializer_class = MovieSerializer







