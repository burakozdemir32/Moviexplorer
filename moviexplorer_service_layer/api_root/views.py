from .models import MovieRatings, Recommendations
from .serializers import MovieRatingsSerializer, UserSerializer

from django.contrib.auth import get_user_model

from rest_framework import viewsets
from rest_framework_jsonp.renderers import JSONPRenderer
from rest_framework import permissions


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
    permission_classes = (permissions.AllowAny, )
    serializer_class = UserSerializer
    model = get_user_model()


class MovieRecommendationView(viewsets.ReadOnlyModelViewSet):
    """
    This endpoint presents top movie information.
    """
    renderer_classes = (JSONPRenderer, )
    serializer_class = MovieRatingsSerializer
    permission_classes = (permissions.IsAuthenticatedOrReadOnly, )

    def get_queryset(self):
        """
        This view should return a list of movie recommendation
        for the current user.
        """
        user_id = self.request.query_params.get('user_id', None)

        if user_id is not None:
            recommendations = Recommendations.objects.filter(user_id=user_id)
            movie_ids = []
            for recommendation in recommendations:
                movie_ids.append(recommendation.movie_id)

            queryset = MovieRatings.objects.filter(movie__id__in=movie_ids)
            return queryset
        else:
            return []


