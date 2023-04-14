from rest_framework import serializers
from bookstore.models import Book, Author, Publisher, Tag, Series, Shelf, Comments
from django.shortcuts import redirect
from django.urls import reverse


class PublisherSerializer(serializers.ModelSerializer):
    class Meta:
        model = Publisher
        fields = '__all__'


class SeriesSerializer(serializers.ModelSerializer):
    class Meta:
        model = Series
        fields = '__all__'


class ShelfSerializer(serializers.ModelSerializer):
    class Meta:
        model = Shelf
        fields = '__all__'


class AuthorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Author
        fields = '__all__'


class TagSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tag
        fields = '__all__'


class CommentsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Comments
        fields = '__all__'


class BookSerializer(serializers.ModelSerializer):
    authors = serializers.HyperlinkedRelatedField(
        many=True,
        read_only=True,
        view_name='api:authors-detail',
    )
    files = serializers.HyperlinkedRelatedField(
        many=True,
        read_only=True,
        view_name='file-download',
    )
    cover_url = serializers.SerializerMethodField()

    def get_cover_url(self, obj: Book):
        if obj.has_cover:
            return reverse('book-cover', args={'pk': obj.pk})
        else:
            return 'static/img/default-cover.jpg'

    class Meta:
        model = Book
        fields = ['id', 'title', 'created_at', 'description', 'authors', 'files', 'cover_url']
