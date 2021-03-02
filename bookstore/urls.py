from django.urls import path
from .views import *

urlpatterns = [
    path('', BookListView.as_view(), name='index'),
    path('books/add/', BookAddView.as_view(), name='book-add'),
    path('book/<int:pk>/', BookDetailView.as_view(), name='book-detail'),
    path('book/<int:pk>/edit', BookEditView.as_view(), name='book-edit'),

    path('authors/', AuthorListView.as_view(), name='author-list'),
    path('author/<int:pk>/', AuthorDetailView.as_view(), name='author-detail'),

    path('tags/', TagListView.as_view(), name='tag-list'),
    path('tag/<int:pk>/', TagDetailView.as_view(), name='tag-detail'),

    path('series/', SeriesListView.as_view(), name='series-list'),
    path('series/<int:pk>/', SeriesDetailView.as_view(), name='series-detail'),

    path('publishers/', PublisherListView.as_view(), name='publisher-list'),
    path('publisher/<int:pk>/', PublisherDetailView.as_view(), name='publisher-detail'),

    path('files/upload', FileUploadView.as_view(), name='file-upload'),
    path('file/<int:file_id>', download_file, name='download_file'),
    path('file/<int:file_id>/delete', file_delete, name='file_delete'),
    path('search/', search, name='search'),
    path('search/<str:subject>', search_subject, name='search_by_subject'),
]
