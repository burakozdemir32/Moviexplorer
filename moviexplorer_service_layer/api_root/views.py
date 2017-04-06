from django.shortcuts import render
from .models import MovieRatings
from .serializers import MovieRatingsSerializer

from rest_framework import viewsets
from rest_framework_jsonp.renderers import JSONPRenderer


class MovieViewSet(viewsets.ReadOnlyModelViewSet):
    """
    This endpoint presents top movie informations.
    """
    renderer_classes = (JSONPRenderer,)

    queryset = MovieRatings.objects.filter().order_by('-average_rating')[:20]
    serializer_class = MovieRatingsSerializer



