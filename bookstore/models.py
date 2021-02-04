from django.db import models


class Book(models.Model):
    title = models.CharField()
    created_at = models.DateTimeField()
    published_at = models.DateField()
    last_modified = models.DateTimeField()
    uuid = models.CharField()
    has_cover = models.BooleanField()
    rating = models.IntegerField()
    description = models.TextField()
    #lang_code = models.

    #publisher
    #seria
    #category


class Publisher(models.Model):
    name = models.CharField()
    link = models.CharField()


class Series(models.Model):
    name = models.CharField()
    description = models.TextField()


class Category(models.Model):
    name = models.CharField()

    #parent_category


class Files(models.Model):
    pass


class User(models.Model):
    username = models.CharField()
    email = models.CharField()
    password_hash = models.CharField()
    #secret
    created_at = models.DateTimeField
    last_login_at = models.DateTimeField
    #is_admin


class Shelf(models.Model):
    name = models.CharField()
    description = models.TextField()
    is_public = models.BooleanField()


class Author(models.Model):
    name = models.CharField()
    description = models.TextField()
    link = models.CharField()


class Identifiers(models.Model):
    name = models.CharField()


class Tags(models.Model):
    name = models.CharField()


