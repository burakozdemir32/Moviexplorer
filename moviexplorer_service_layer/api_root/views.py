from .models import MovieRatings, Recommendations, UserRatings
from .serializers import MovieRatingsSerializer, UserSerializer, UserRatingsSerializer

from django.contrib.auth import get_user_model

from rest_framework import viewsets, permissions, status
from rest_framework_jsonp.renderers import JSONPRenderer
from rest_framework.response import Response

class MovieSearchView(viewsets.ReadOnlyModelViewSet):
    """
    This endpoint presents top movie information.
    """
    renderer_classes = (JSONPRenderer, )
    serializer_class = MovieRatingsSerializer
    permission_classes = (permissions.IsAuthenticatedOrReadOnly, )

    def get_queryset(self):
        """
        This view should return a list of movies 
        for the currently searched movie title.
        """
        title = self.request.query_params.get('title', None)

        if title is not None:
            queryset = MovieRatings.objects.filter(
                movie__title__icontains=title
            )
            return queryset
        else:
            return []


class CreateUserView(viewsets.generics.CreateAPIView):
    """
    This endpoint allows users to register to the system.
    """
    permission_classes = (permissions.AllowAny, )
    serializer_class = UserSerializer
    model = get_user_model()


class UserRatingsView(viewsets.generics.CreateAPIView):
    """
    This endpoint allows users to rate movies.
    """
    permission_classes = (permissions.AllowAny,)
    serializer_class = UserRatingsSerializer
    model = UserRatings

    def create(self, request, *args, **kwargs):
        user_id = get_user_model().objects.get(username=request.data['username']).id
        data = {'user_id': user_id, 'rating': request.data['rating'], 'movie': request.data['movie']}
        serializer = self.get_serializer(data=data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        rating = UserRatings.objects.get(id=serializer.instance.id)
        return Response({'id': rating.id}, status=status.HTTP_201_CREATED, headers=headers)


class MovieRecommendationView(viewsets.ReadOnlyModelViewSet):
    """
    This endpoint makes movie recommendations.
    """
    serializer_class = MovieRatingsSerializer
    permission_classes = (permissions.IsAuthenticated, )

    def get_queryset(self):
        """
        This view should return a list of movie recommendation
        for the current user.
        """
        username = self.request.query_params.get('username', None)

        if username is not None:
            user = get_user_model().objects.get(username=username)
            recommendations = Recommendations.objects.filter(user_id=user.id)
            movie_ids = []
            for recommendation in recommendations:
                movie_ids.append(recommendation.movie_id)

            queryset = MovieRatings.objects.filter(movie__id__in=movie_ids)
            return queryset
        else:
            return []
