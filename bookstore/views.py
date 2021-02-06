from django.shortcuts import render, redirect, reverse
from bookstore.models import Book, Author
from bookstore.forms import BookForm


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
    payload['author'] = Author.objects.get(pk=author_id)
    payload['title'] = payload['author'].name + " books"

    return render(request, 'author_page.html', payload)


def book_add(request):
    payload = dict()
    payload['title'] = "Book add"

    form = BookForm(request.POST or None)
    if request.method == "POST":
        if form.is_valid():
            book = form.save()
            return redirect(reverse('book_page', kwargs={'book_id': book.id}))

    payload['form'] = form
    return render(request, 'book_add.html', payload)


def book_page(request, book_id):
    payload = dict()
    payload['book'] = Book.objects.get(pk=book_id)
    payload['title'] = payload['book'].title + " books"

    return render(request, 'book_page.html', payload)


def book_edit(request, book_id):
    payload = dict()
    book = Book.objects.get(pk=book_id)

    form = BookForm(request.POST or None, instance=book)
    if request.method == "POST":
        if form.is_valid():
            book = form.save()
            return redirect(reverse('book_page', kwargs={'book_id': book.id}))

    payload['title'] = book.title + " edit"
    payload['form'] = form
    return render(request, 'book_add.html', payload)
