from rest_framework import filters, mixins
from rest_framework.pagination import LimitOffsetPagination
from rest_framework.viewsets import GenericViewSet

from .permissions import AdminCreateDeleteOrReadOnly


class ListCreateDestroyViewSet(mixins.CreateModelMixin,
                               mixins.DestroyModelMixin,
                               mixins.ListModelMixin,
                               GenericViewSet):
    pass


class AdminControlSlugViewSet(ListCreateDestroyViewSet):
    '''Общий родительский класс для категорий и жанров.'''
    filter_backends = [filters.SearchFilter]
    search_fields = ('=name', )
    lookup_field = 'slug'
    permission_classes = (AdminCreateDeleteOrReadOnly,)
    pagination_class = LimitOffsetPagination
