from django.urls import path
from .views import *

urlpatterns = [
    path('', BookListView.as_view(), name='index'),
    path('books/search', BookSearchView.as_view(), name='book-search'),
    path('book/<int:pk>', BookDetailView.as_view(), name='book-detail'),
    path('book/<int:pk>/edit', BookEditView.as_view(), name='book-edit'),
    path('book/<int:pk>/delete', BookEditView.as_view(), name='book-delete'),

    path('authors', AuthorListView.as_view(), name='author-list'),
    path('authors/add', AuthorCreateView.as_view(), name='author-create'),
    path('authors/search', AuthorSearchView.as_view(), name='author-search'),
    path('author/<int:pk>', AuthorDetailView.as_view(), name='author-detail'),
    path('author/<int:pk>/edit', AuthorEditView.as_view(), name='author-edit'),
    path('author/<int:pk>/delete', AuthorDeleteView.as_view(), name='author-delete'),

    path('tags', TagListView.as_view(), name='tag-list'),
    path('tags/add', TagCreateView.as_view(), name='tag-create'),
    path('tags/search', TagSearchView.as_view(), name='tag-search'),
    path('tag/<int:pk>', TagDetailView.as_view(), name='tag-detail'),
    path('tag/<int:pk>/edit', TagEditView.as_view(), name='tag-edit'),
    path('tag/<int:pk>/delete', TagDeleteView.as_view(), name='tag-delete'),

    path('series', SeriesListView.as_view(), name='series-list'),
    path('series/add', SeriesCreateView.as_view(), name='series-create'),
    path('series/search', SeriesSearchView.as_view(), name='series-search'),
    path('series/<int:pk>', SeriesDetailView.as_view(), name='series-detail'),
    path('series/<int:pk>/edit', SeriesEditView.as_view(), name='series-edit'),
    path('series/<int:pk>/delete', SeriesDeleteView.as_view(), name='series-delete'),

    path('publishers', PublisherListView.as_view(), name='publisher-list'),
    path('publishers/add', PublisherCreateView.as_view(), name='publisher-create'),
    path('publishers/search', PublisherSearchView.as_view(), name='publishers-search'),
    path('publisher/<int:pk>', PublisherDetailView.as_view(), name='publisher-detail'),
    path('publisher/<int:pk>/edit', PublisherEditView.as_view(), name='publisher-edit'),
    path('publisher/<int:pk>/delete', PublisherDeleteView.as_view(), name='publisher-delete'),

    path('statistic', StatisticView.as_view(), name='statistic'),

    path('files/upload', FileUploadView.as_view(), name='file-upload'),
    path('file/<int:pk>', FileDownloadView.as_view(), name='file-download'),
    path('file/<int:pk>/delete', FileDeleteView.as_view(), name='file-delete'),

    path('cover/<int:pk>', BookCoverView.as_view(), name='book-cover'),

    path('search', SearchView.as_view(), name='search')
]

