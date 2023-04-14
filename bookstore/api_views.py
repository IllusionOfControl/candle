from rest_framework import (
    routers,
    viewsets,
    views,
    authentication,
    generics,
    status,
    decorators,
)
from bookstore.models import Book, Author, Publisher, Tag, Series, Shelf, Comments
from bookstore.serializers import BookSerializer, AuthorSerializer, PublisherSerializer, TagSerializer, ShelfSerializer, \
    SeriesSerializer, CommentsSerializer

router = routers.DefaultRouter()
app_name = 'Candle'


class BookViewSet(viewsets.ModelViewSet):
    queryset = Book.objects.all()
    serializer_class = BookSerializer


class AuthorViewSet(viewsets.ModelViewSet):
    queryset = Author.objects.all()
    serializer_class = AuthorSerializer


class PublisherViewSet(viewsets.ModelViewSet):
    queryset = Publisher.objects.all()
    serializer_class = PublisherSerializer


class SeriesViewSet(viewsets.ModelViewSet):
    queryset = Series.objects.all()
    serializer_class = SeriesSerializer


class ShelfViewSet(viewsets.ModelViewSet):
    queryset = Shelf.objects.all()
    serializer_class = ShelfSerializer


class TagViewSet(viewsets.ModelViewSet):
    queryset = Tag.objects.all()
    serializer_class = TagSerializer


router.register('books', BookViewSet, 'books')
router.register('authors', AuthorViewSet, 'authors')
router.register('publisher', PublisherViewSet, 'publishers')
router.register('series', SeriesViewSet, 'series')
router.register('shelves', ShelfViewSet, 'shelves')
router.register('tags', TagViewSet, 'tags')
