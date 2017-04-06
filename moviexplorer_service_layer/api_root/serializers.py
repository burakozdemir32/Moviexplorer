from .models import Movie, MovieRatings, MovieActorIndex, MovieDirectorIndex, Person

from rest_framework import serializers


class MovieSerializer(serializers.ModelSerializer):
    class Meta:
        model = Movie
        exclude = ('id',)


class MovieRatingsSerializer(serializers.ModelSerializer):
    movie = MovieSerializer(read_only=True)

    class Meta:
        model = MovieRatings
        exclude = ('id',)
