from django.urls import path
from .views import *

urlpatterns = [
    path('', BookListView.as_view(), name='index'),
    path('books/add/', BookAddView.as_view(), name='book-add'),
    path('book/<int:book_id>/', book_page, name='book-detail'),
    path('book/<int:book_id>/edit', book_edit, name='book-edit'),

    path('authors/', author_list, name='author-list'),
    path('author/<int:author_id>/', author_page, name='author-detail'),

    path('tags/', tag_list, name='tag-list'),
    path('tag/<int:tag_id>/', tag_page, name='tag-detail'),

    path('series/', series_list, name='series-list'),
    path('series/<int:series_id>/', series_page, name='series-detail'),

    path('publishers/', publisher_list, name='publisher-list'),
    path('publisher/<int:publisher_id>/', publisher_page, name='publisher-detail'),

    path('auth/login', auth_login, name='auth_login'),
    path('auth/logout', auth_logout, name='auth_logout'),
    path('auth/register', auth_register, name='auth_register'),

    path('file/<int:file_id>', download_file, name='download_file'),
    path('file/<int:file_id>/delete', file_delete, name='file_delete'),
    path('search/', search, name='search'),
    path('search/<str:subject>', search_subject, name='search_by_subject'),
]
