from django.db import models


class Publisher(models.Model):
    name = models.CharField()
    link = models.CharField()


class Series(models.Model):
    name = models.CharField()
    description = models.TextField()


class Shelf(models.Model):
    name = models.CharField()
    description = models.TextField()
    is_public = models.BooleanField()


class Author(models.Model):
    name = models.CharField()
    description = models.TextField()
    link = models.CharField()


class Tag(models.Model):
    name = models.CharField()


class User(models.Model):
    username = models.CharField()
    email = models.CharField()
    password_hash = models.CharField()
    is_banned = models.BooleanField()
    created_at = models.DateTimeField()
    last_login_at = models.DateTimeField()


class Book(models.Model):
    title = models.CharField()
    created_at = models.DateTimeField()
    published_at = models.DateField()
    last_modified = models.DateTimeField()
    uuid = models.CharField()
    has_cover = models.BooleanField()
    rating = models.IntegerField()
    description = models.TextField()

    publisher = models.ForeignKey(Publisher)
    series = models.ForeignKey(Series)

    tags = models.ManyToManyField(Tag)
    shelves = models.ManyToManyField(Shelf)


class File(models.Model):
    uuid = models.CharField()
    extension = models.CharField()
    md5 = models.CharField()
    size = models.IntegerField()

    book = models.ForeignKey(Book, on_delete=models.CASCADE)
    uploader = models.ForeignKey(User, on_delete=models.CASCADE)


class Identifier(models.Model):
    name = models.CharField()
    value = models.CharField()

    book = models.ForeignKey(Book)
