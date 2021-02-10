from django.shortcuts import render, redirect, reverse
from django.http import Http404, HttpResponse
from django.core.files.storage import default_storage
from django.utils.text import get_valid_filename
from django.db.models import Q
from django.contrib import messages
from django.core.paginator import Paginator
from bookstore.models import *
from bookstore.forms import BookForm
import mimetypes


def index(request):
    page_num = request.GET.get('page', 1)
    payload = dict()
    payload['books'] = Book.objects.all()
    paginator = Paginator(payload['books'], 30)
    payload['books'] = paginator.get_page(page_num)
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

            files = request.FILES.getlist('files')

            for f in files:
                ext = mimetypes.guess_extension(f.content_type)
                size = f.size

                old_file = File.objects.filter(book=book, extension=ext).first()
                if old_file:
                    default_storage.delete(old_file.uuid)
                    old_file.delete()
                new_file = File(book=book,
                                extension=ext,
                                md5='1', size=size,
                                uploader=request.user)
                new_file.save()
                default_storage.save(new_file.uuid, f)

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

            files = request.FILES.getlist('files')

            for f in files:
                ext = mimetypes.guess_extension(f.content_type)
                size = f.size

                old_file = File.objects.filter(book=book, extension=ext).first()
                if old_file:
                    default_storage.delete(old_file.uuid)
                    old_file.delete()
                new_file = File(book=book,
                                extension=ext,
                                md5='1', size=size,
                                uploader=request.user)
                default_storage.save(new_file.uuid, f)
                new_file.save()

            return redirect(reverse('book_page', kwargs={'book_id': book.id}))

    payload['title'] = book.title + " edit"
    payload['files'] = book.files.all()
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


def download_file(request, file_id):
    file = File.objects.get(id=file_id)
    if file:
        response = HttpResponse(default_storage.open(file.uuid).read(),
                                content_type=mimetypes.guess_type(file.extension))
        filename = get_valid_filename(file.book.title + file.extension)
        response['Content-Disposition'] = 'attachment; filename=' + filename
        return response
    return Http404


def search(request):
    query = request.GET.get('query', '')
    if len(query) < 3:
        messages.info(request, 'Query must have min 3 character!')
        return redirect(request.META.get('HTTP_REFERER'))
    payload = dict()
    payload['query'] = query
    payload['books'] = Book.objects.filter(Q(title__contains=query, description__contains=query))[:5]
    payload['authors'] = Author.objects.filter(Q(name__contains=query))[:5]
    payload['publishers'] = Publisher.objects.filter(Q(name__contains=query))[:5]
    payload['series'] = Series.objects.filter(Q(name__contains=query))[:5]
    payload['tags'] = Tag.objects.filter(Q(name__contains=query))[:5]

    payload['title'] = "Result search by " + query

    return render(request, 'search_page.html', payload)


def search_subject(request, subject):
    query = request.GET.get('query', '')
    if len(query) < 3:
        messages.info(request, 'Query must have min 3 character!')
        return redirect(request.META.get('HTTP_REFERER'))
    elif subject == 'books':
        model_filter = Q(title__contains=query, description__contains=query)
        model = Book
    elif subject == 'author':
        model_filter = Q(name__contains=query)
        model = Author
    # etc:
    else:
        return Http404

    objects = model.objects.filter(model_filter)
    payload = dict()
    payload['subject'] = subject
    payload[subject] = objects
    payload['title'] = "Result search by " + query
    return render(request, 'search_by_subject.html', payload)


def file_delete(request, file_id):
    file = File.objects.get(id=file_id)
    if not file:
        return Http404
    book_id = file.book.id
    default_storage.delete(file.uuid)
    file.delete()
    return redirect(reverse('book_edit', kwargs={'book_id': book_id}))


###
#
#   AUTH
#
###

from django.contrib.auth.forms import AuthenticationForm, UserCreationForm
from django.contrib.auth import login, logout


def auth_login(request):
    if request.method == "POST":
        form = AuthenticationForm(request, request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            return redirect(reverse('index'))

    payload = dict()
    payload['form'] = AuthenticationForm()
    payload['title'] = 'Login page'
    return render(request, 'auth/login.html', payload)


def auth_logout(request):
    if request.user.is_authenticated:
        logout(request)
    return redirect(reverse('index'))


def auth_register(request):
    if request.method == "POST":
        form = UserCreationForm(request.POST, request)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect(reverse('index'))
        print(form.errors)

    payload = dict()
    payload['form'] = UserCreationForm()
    payload['title'] = 'Register page'
    return render(request, 'auth/register.html', payload)

