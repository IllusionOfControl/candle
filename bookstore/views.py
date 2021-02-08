from django.shortcuts import render, redirect, reverse
from bookstore.models import *
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

    form = BookForm(request.POST or None,
                    request.FILES or None)
    if request.method == "POST":
        if form.is_valid():
            book = form.save()

            ext = request.FILES['file'].content_type.split('/')[-1]
            size = request.FILES['file'].size
            file = File(book=book, extension=ext, md5='1', size=size, uploader=request.user, uuid='1')
            file.save()

            print('file saved')
            return redirect(reverse('book_page', kwargs={'book_id': book.id}))
        print('form is not valid')

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


def tag_list(request):
    payload = dict()
    payload['tags'] = Tag.objects.all()
    payload['title'] = "Tag list"

    return render(request, 'tags.html', payload)


def tag_page(request, tag_id):
    payload = dict()
    payload['tag'] = Tag.objects.get(pk=tag_id)
    payload['title'] = payload['tag'].name + " books"

    return render(request, 'tag_page.html', payload)
