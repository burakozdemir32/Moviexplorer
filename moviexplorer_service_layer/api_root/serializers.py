from .models import Movie, MovieRatings
from django.contrib.auth import get_user_model

from rest_framework import serializers
from rest_framework.validators import UniqueValidator


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
    email = serializers.EmailField(required=True, validators=[
        UniqueValidator(
            queryset=get_user_model().objects.all(),
            message="A user with that email address already exists.",
        )]
    )

    def create(self, validated_data):
        user = get_user_model().objects.create(
            username=validated_data['username'], email=validated_data['email']
        )
        user.set_password(validated_data['password'])
        user.save()

        return user

    class Meta:
        model = get_user_model()
        fields = ('username', 'password', 'email')

