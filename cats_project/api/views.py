from rest_framework import viewsets

from cats.models import Breed, Cat, Score
from .filters import BreedFilter
from .permissions import AdminOrReadOnly, ReadOnlyOrAuthor
from .serializers import (BreedSerializer, CatSerializer,
                          ScoreSerializer)


class BreedViewSet(viewsets.ModelViewSet):
    queryset = Breed.objects.all()
    serializer_class = BreedSerializer
    permission_classes = (AdminOrReadOnly,)
    lookup_field = 'slug'


class CatViewSet(viewsets.ModelViewSet):
    queryset = Cat.objects.select_related(
        'breed', 'owner'
    ).all()
    serializer_class = CatSerializer
    permission_classes = (ReadOnlyOrAuthor,)
    filter_backends = (BreedFilter,)
    http_method_names = ['get', 'post', 'patch', 'delete']

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)


class ScoreViewSet(viewsets.ModelViewSet):
    queryset = Score.objects.select_related(
        'owner', 'cat'
    ).all()
    serializer_class = ScoreSerializer
    permission_classes = (ReadOnlyOrAuthor,)
    http_method_names = ['get', 'post', 'patch', 'delete']

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)
