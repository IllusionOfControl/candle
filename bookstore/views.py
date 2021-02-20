from django.shortcuts import render, redirect, reverse
from django.http import Http404, HttpResponse
from django.core.files.storage import default_storage
from django.utils.text import get_valid_filename
from django.db.models import Q
from django.contrib import messages
from django.core.paginator import Paginator
from django.views.generic.list import ListView
from django.views.generic.edit import CreateView, UpdateView
from django.views.generic.detail import DetailView
from django.conf import settings
from bookstore.models import *
from bookstore.forms import BookForm
import mimetypes


class BookListView(ListView):
    model = Book
    template_name = 'book_list.html'
    paginate_by = settings.ITEMS_PER_PAGE
    context_object_name = 'books'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = "Book list"
        return context


class BookDetailView(DetailView):
    model = Book
    template_name = 'book_detail.html'
    context_object_name = 'book'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = '{} - detail'.format(self.object.title)
        return context


class BookAddView(CreateView):
    template_name = 'book_editor.html'
    model = Book
    form_class = BookForm

    def get_success_url(self):
        return reverse('book-detail', kwargs={'book_id': self.object.pk})

    def form_valid(self, form):
        response = super().form_valid(form)
        files = self.request.FILES.getlist('files')
        for f in files:
            ext = mimetypes.guess_extension(f.content_type)
            size = f.size
            new_file = File(book=self.object,
                            extension=ext,
                            md5='1', size=size,
                            uploader=self.request.user)
            new_file.save()
            default_storage.save(new_file.uuid, f)

        return response


class BookEditView(UpdateView):
    template_name = 'book_editor.html'
    model = Book
    form_class = BookForm

    def get_success_url(self):
        return reverse('book-detail', kwargs={'pk': self.object.pk})

    def form_valid(self, form):
        response = super().form_valid(form)
        files = self.request.FILES.getlist('files')
        for f in files:
            ext = mimetypes.guess_extension(f.content_type)
            size = f.size

            old_file = File.objects.filter(book=self.object, extension=ext).first()
            if old_file:
                default_storage.delete(old_file.uuid)
                old_file.delete()

            new_file = File(book=self.object,
                            extension=ext,
                            md5='1', size=size,
                            uploader=self.request.user)
            new_file.save()
            default_storage.save(new_file.uuid, f)

        return response


class AuthorListView(ListView):
    model = Author
    template_name = 'author_list.html'
    context_object_name = 'authors'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = "Author List"
        return context


class AuthorDetailView(DetailView):
    model = Author
    template_name = 'author_detail.html'
    context_object_name = 'author'
    paginate_by = settings.ITEMS_PER_PAGE

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = '{} - detail'.format(self.object.name)
        return context


class TagListView(ListView):
    model = Tag
    template_name = 'tag_list.html'
    context_object_name = 'tags'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Author List'
        return context


class TagDetailView(DetailView):
    model = Tag
    template_name = 'tag_detail.html'
    context_object_name = 'tag'
    paginate_by = settings.ITEMS_PER_PAGE

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Tag "{}" - detail'.format(self.object.name)
        return context


class SeriesListView(ListView):
    model = Series
    template_name = 'series_list.html'
    context_object_name = 'series'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Series List'
        return context


class SeriesDetailView(DetailView):
    model = Author
    template_name = 'series_page.html'
    context_object_name = 'series'
    paginate_by = settings.ITEMS_PER_PAGE

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Book series "{}" - detail'.format(self.object.name)
        return context


class PublisherListView(ListView):
    model = Publisher
    template_name = 'publisher_list.html'
    context_object_name = 'publishers'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Publisher List'
        return context


class PublisherDetailView(DetailView):
    model = Publisher
    template_name = 'publisher_detail.html'
    context_object_name = 'publisher'
    paginate_by = settings.ITEMS_PER_PAGE

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Publisher "{}" - detail'.format(self.object.name)
        return context


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
    return redirect(reverse('book-edit', kwargs={'book_id': book_id}))


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

