from .models import MovieRatings
from .serializers import MovieRatingsSerializer

from rest_framework import viewsets
from rest_framework_jsonp.renderers import JSONPRenderer


class MovieViewSet(viewsets.ReadOnlyModelViewSet):
    """
    This endpoint presents top movie informations.
    """
    renderer_classes = (JSONPRenderer,)
    serializer_class = MovieRatingsSerializer

    def get_queryset(self):
        """
        This view should return a list of all the purchases
        for the currently authenticated user.
        """
        queryset = MovieRatings.objects.all()\
            .order_by('-average_rating')\
            .exclude(average_rating=None)

        title = self.request.query_params.get('title', None)
        if title is not None:
            queryset = queryset.filter(movie__title__icontains=title)
        return queryset


