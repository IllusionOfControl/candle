from django.db import models
from django.contrib.auth.models import User
import uuid


class Publisher(models.Model):
    name = models.CharField(max_length=64)
    link = models.CharField(max_length=256)


class Series(models.Model):
    name = models.CharField(max_length=64)
    description = models.TextField()

    class Meta:
        verbose_name_plural = 'Series'


class Shelf(models.Model):
    name = models.CharField(max_length=64)
    description = models.TextField()
    is_public = models.BooleanField()


class Author(models.Model):
    name = models.CharField(max_length=64)
    link = models.CharField(max_length=256)
    description = models.TextField()


class Tag(models.Model):
    name = models.CharField(max_length=32)


class Book(models.Model):
    title = models.CharField(max_length=128)
    created_at = models.DateTimeField(auto_now_add=True)
    published_at = models.DateField(null=True)
    last_modified = models.DateTimeField(auto_now=True)
    uuid = models.CharField(max_length=36)
    has_cover = models.BooleanField(default=False)
    rating = models.IntegerField(default=0)
    description = models.TextField()

    publisher = models.ForeignKey(Publisher, on_delete=models.SET_NULL, null=True, related_name='books')
    series = models.ForeignKey(Series, on_delete=models.SET_NULL, null=True, related_name='books')
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, related_name='books')

    authors = models.ManyToManyField(Author, related_name='books')
    tags = models.ManyToManyField(Tag, related_name='books')
    shelves = models.ManyToManyField(Shelf, related_name='books')

    def get_authors(self):
        return self.authors.all()


class Comments(models.Model):
    timestamp = models.DateTimeField(auto_now_add=True)
    content = models.TextField()

    book = models.ForeignKey(Book, on_delete=models.CASCADE,  related_name='comments')
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='comments')


class File(models.Model):
    uuid = models.CharField(max_length=36, default=uuid.uuid4().hex)
    extension = models.CharField(max_length=8)
    md5 = models.CharField(max_length=32)
    size = models.IntegerField()

    book = models.ForeignKey(Book, on_delete=models.CASCADE, related_name='files')
    uploader = models.ForeignKey(User, on_delete=models.CASCADE, related_name='files')


class Identifier(models.Model):
    name = models.CharField(max_length=24)
    value = models.CharField(max_length=24)

    book = models.ForeignKey(Book, on_delete=models.CASCADE, related_name='identifiers')
