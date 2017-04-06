from .models import MovieRatings
from .serializers import MovieRatingsSerializer

from rest_framework import viewsets
from rest_framework_jsonp.renderers import JSONPRenderer


class MovieViewSet(viewsets.ReadOnlyModelViewSet):
    """
    This endpoint presents top movie informations.
    """
    renderer_classes = (JSONPRenderer,)

    queryset = MovieRatings.objects.filter(
        imdb_votes__gte=1000,
        tomato_user_reviews__gte=1000,
        tomato_reviews__gte=1
    ).order_by('-average_rating')[:500]
    serializer_class = MovieRatingsSerializer



