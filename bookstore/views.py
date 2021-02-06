from django.shortcuts import render
from bookstore.models import Book, Author


def index(request):
    payload = dict()
    payload['books'] = Book.objects.all()
    payload['title'] = "Book list"

    return render(request, 'index.html', payload)


def author_list(request):
    payload = dict()
    payload['authors'] = Author.objects.all()
    payload['title'] = "Author list"

    return render(request, 'authors.html', payload)


def author_page(request, author_id):
    payload = dict()
    payload['author'] = Author.objects.all()
    payload['title'] = "Author list"
