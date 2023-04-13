from django.contrib.auth.models import User
from django.db import models
from django.db.models import Q
import uuid


class SearchMixin:
    search_field = None

    def search(self, query=None):
        queryset = self.get_queryset()
        if query:
            key = "{}__contains".format(self.search_field)
            or_lookup = (Q(**{key: query}))
            queryset = queryset.filter(or_lookup)

        return queryset


class BookManager(SearchMixin, models.Manager):
    search_field = "title"


class AuthorManager(SearchMixin, models.Manager):
    search_field = "name"


class TagManager(SearchMixin, models.Manager):
    search_field = "name"


class SeriesManager(SearchMixin, models.Manager):
    search_field = "title"


class PublisherManager(SearchMixin, models.Manager):
    search_field = "name"


class Publisher(models.Model):
    objects = PublisherManager()

    name = models.CharField(max_length=64)
    link = models.CharField(max_length=256)

    def __str__(self):
        return self.name

    class Meta:
        ordering = ['name']


class Series(models.Model):
    objects = SeriesManager()

    title = models.CharField(max_length=64)
    description = models.TextField()

    class Meta:
        ordering = ['title']
        verbose_name_plural = 'Series'

    def __str__(self):
        return self.title


class Shelf(models.Model):
    name = models.CharField(max_length=64)
    description = models.TextField()
    is_public = models.BooleanField()

    def __str__(self):
        return self.name


class Author(models.Model):
    objects = AuthorManager()

    name = models.CharField(max_length=64)
    link = models.CharField(max_length=256)
    description = models.TextField()

    def __str__(self):
        return self.name

    class Meta:
        ordering = ['name']


class Tag(models.Model):
    objects = TagManager()

    name = models.CharField(max_length=32)

    def __str__(self):
        return self.name

    class Meta:
        ordering = ['name']


class Book(models.Model):
    objects = BookManager()

    title = models.CharField(max_length=128, default='Untitled book')
    created_at = models.DateTimeField(auto_now_add=True)
    published_at = models.DateField(null=True)
    last_modified = models.DateTimeField(auto_now=True)
    uuid = models.UUIDField(default=uuid.uuid4, editable=False)
    has_cover = models.BooleanField(default=False)
    description = models.TextField()
    isbn = models.CharField(max_length=16, blank=True)

    publisher = models.ForeignKey(Publisher, on_delete=models.SET_NULL, null=True, related_name='books', blank=True)
    series = models.ForeignKey(Series, on_delete=models.SET_NULL, null=True, related_name='books', blank=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, related_name='books', blank=True)

    authors = models.ManyToManyField(Author, related_name='books', blank=True)
    tags = models.ManyToManyField(Tag, related_name='books', blank=True)
    shelves = models.ManyToManyField(Shelf, related_name='books')

    class Meta:
        ordering = ['-pk']

    def get_authors(self):
        return self.authors.all()

    def __str__(self):
        return self.title


class Comments(models.Model):
    timestamp = models.DateTimeField(auto_now_add=True)
    content = models.TextField()

    book = models.ForeignKey(Book, on_delete=models.CASCADE, related_name='comments')
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='comments')


class File(models.Model):
    uuid = models.UUIDField(default=uuid.uuid4)
    extension = models.CharField(max_length=8)
    size = models.IntegerField()

    book = models.ForeignKey(Book, on_delete=models.CASCADE, related_name='files')
    uploader = models.ForeignKey(User, on_delete=models.CASCADE, related_name='files')

    def __str__(self):
        return self.uuid
