from .models import Movie, MovieRatings, Recommendations
from django.contrib.auth import get_user_model

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


class UserSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)

    def create(self, validated_data):
        user = get_user_model().objects.create(
            username=validated_data['username']
        )
        user.set_password(validated_data['password'])
        user.save()

        return user

    class Meta:
        model = get_user_model()
        fields = ('username', 'password')


class RecommendationSerializer(serializers.ModelSerializer):
    def to_representation(self, data):
        r = super().to_representation(data)

        return r['movie_id']

    class Meta:
        model = Recommendations
        fields = ('movie_id',)
