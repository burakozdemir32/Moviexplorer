from .models import Movie, MovieRatings, UserRatings
from django.contrib.auth import get_user_model

from rest_framework import serializers
from rest_framework.validators import UniqueValidator


class MovieSerializer(serializers.ModelSerializer):
    class Meta:
        model = Movie
        fields = '__all__'


class MovieRatingsSerializer(serializers.ModelSerializer):
    movie = MovieSerializer(read_only=True)

    class Meta:
        model = MovieRatings
        fields = '__all__'


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
        fields = '__all__'


class UserRatingsSerializer(serializers.ModelSerializer):
    def create(self, validated_data):
        user_rating = UserRatings(
            user_id=validated_data['user_id'],
            rating=validated_data['rating'],
            movie=validated_data['movie']
        )

        user_rating.save()
        return user_rating

    class Meta:
        model = UserRatings
        fields = '__all__'
