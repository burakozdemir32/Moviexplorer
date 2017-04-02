from .models import Movie, MovieRatings, MovieActorIndex, MovieDirectorIndex, Person

from rest_framework import serializers


class MovieSerializer(serializers.ModelSerializer):
    class Meta:
        model = Movie
        fields = '__all__'
