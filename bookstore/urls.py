from django.urls import path
from .views import index, author_list, author_page, book_add, book_page

urlpatterns = [
    path('', index, name='index'),
    path('authors/', author_list, name='authors'),
    path('author/<int:author_id>/', author_page, name='author_page'),
    path('books/add/', book_add, name='book_add'),
    path('book/<int:book_id>/', book_page, name='book_page')
]
