from django.urls import path
from .views import *

urlpatterns = [
    path('', index, name='index'),
    path('authors/', author_list, name='authors'),
    path('author/<int:author_id>/', author_page, name='author_page'),
    path('books/add/', book_add, name='book_add'),
    path('book/<int:book_id>/', book_page, name='book_page'),
    path('book/<int:book_id>/edit', book_edit, name='book_edit'),
    path('tags/', tag_list, name='tag_list'),
    path('tag/<int:tag_id>/', tag_page, name='tag_page'),
    path('series/', series_list, name='series_list'),
    path('series/<int:series_id>/', series_page, name='series_info'),
    path('publishers/', publisher_list, name='publisher_list'),
    path('publisher/<int:publisher_id>/', publisher_page, name='publisher_info'),

    path('auth/login', auth_login, name='auth_login'),
    path('auth/logout', auth_logout, name='auth_logout'),
    path('auth/register', auth_register, name='auth_register')
]
