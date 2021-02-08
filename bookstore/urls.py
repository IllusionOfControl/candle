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

]
