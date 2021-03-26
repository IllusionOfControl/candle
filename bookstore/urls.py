from django.urls import path
from .views import *

urlpatterns = [
    path('', BookListView.as_view(), name='index'),
    path('books/search', BookSearchView.as_view(), name='book-search'),
    path('books/add', BookAddView.as_view(), name='book-add'),
    path('book/<int:pk>', BookDetailView.as_view(), name='book-detail'),
    path('book/<int:pk>/edit', BookEditView.as_view(), name='book-edit'),

    path('authors', AuthorListView.as_view(), name='author-list'),
    path('authors/search', AuthorSearchView.as_view(), name='author-search'),
    path('author/<int:pk>', AuthorDetailView.as_view(), name='author-detail'),

    path('tags', TagListView.as_view(), name='tag-list'),
    path('tag/<int:pk>', TagDetailView.as_view(), name='tag-detail'),

    path('series', SeriesListView.as_view(), name='series-list'),
    path('series/<int:pk>', SeriesDetailView.as_view(), name='series-detail'),

    path('publishers', PublisherListView.as_view(), name='publisher-list'),
    path('publisher/<int:pk>', PublisherDetailView.as_view(), name='publisher-detail'),

    path('files/upload', FileUploadView.as_view(), name='file-upload'),
    path('file/<int:pk>', FileDownloadView.as_view(), name='file-download'),
    path('file/<int:pk>/delete', FileDeleteView.as_view(), name='file-delete'),

    path('cover/<int:pk>', BookCoverView.as_view(), name='book-cover'),

    path('search', SearchView.as_view(), name='search'),
    path('search/<str:subject>', search_subject, name='search_by_subject'),
]

