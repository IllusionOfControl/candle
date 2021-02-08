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

            import mimetypes

            files = request.FILES.getlist('files')

            from django.core.files.storage import default_storage

            for f in files:
                ext = mimetypes.guess_extension(f.content_type)
                size = f.size
                filename = book.title + "." + ext
                default_storage.save(filename, f)
                File(book=book,
                     extension=ext,
                     md5='1', size=size,
                     uploader=request.user,
                     uuid='1').save()

            print('file saved')
            print(form.files)
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

    form = BookForm(request.POST or None,
                    request.FILES or None,
                    instance=book)
    if request.method == "POST":
        if form.is_valid():
            book = form.save()

            import mimetypes

            files = request.FILES.getlist('files')

            from django.core.files.storage import default_storage

            for f in files:
                ext = mimetypes.guess_extension(f.content_type)
                size = f.size
                filename = book.title + "." + ext
                if default_storage.exists(filename):
                    default_storage.delete(filename)
                default_storage.save(filename, f)
                File(book=book,
                     extension=ext,
                     md5='1', size=size,
                     uploader=request.user,
                     uuid='1').save()
            return redirect(reverse('book_page', kwargs={'book_id': book.id}))
        print(form.errors)

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


def series_list(request):
    payload = dict()
    payload['series'] = Series.objects.all()
    payload['title'] = "Series list"

    return render(request, 'series.html', payload)


def series_page(request, series_id):
    payload = dict()
    payload['series'] = Series.objects.get(pk=series_id)
    payload['title'] = payload['series'].name + " books"

    return render(request, 'series_page.html', payload)


def publisher_list(request):
    payload = dict()
    payload['publishers'] = Publisher.objects.all()
    payload['title'] = "Publisher list"

    return render(request, 'publishers.html', payload)


def publisher_page(request, publisher_id):
    payload = dict()
    payload['publisher'] = Publisher.objects.get(pk=publisher_id)
    payload['title'] = payload['publisher'].name + " books"

    return render(request, 'publisher_page.html', payload)
