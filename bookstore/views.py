from django.shortcuts import render, redirect, reverse
from django.http import Http404, HttpResponse
from django.core.files.storage import default_storage
from django.utils.text import get_valid_filename
from django.db.models import Q
from django.contrib import messages
from django.views.generic.list import ListView
from django.views.generic.edit import CreateView, UpdateView, FormView
from django.views.generic.detail import DetailView
from django.conf import settings
from bookstore.models import *
from bookstore.forms import BookForm, FileUploadForm
import mimetypes


class BookListView(ListView):
    model = Book
    template_name = 'book_list.html'
    paginate_by = settings.ITEMS_PER_PAGE
    extra_context = {'title': 'Book list'}
    context_object_name = 'books'


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

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = '{} - add'.format(self.object.title)
        return context

    def form_valid(self, form):
        response = super().form_valid(form)
        files = self.request.FILES.getlist('files')
        for f in files:
            ext = mimetypes.guess_extension(f.content_type)
            size = f.size
            new_file = File(book=self.object,
                            extension=ext,
                            size=size,
                            uploader=self.request.user)
            new_file.save()
            default_storage.save(new_file.uuid.hex, f)

        return response


class BookEditView(UpdateView):
    template_name = 'book_editor.html'
    model = Book
    form_class = BookForm

    def get_success_url(self):
        return reverse('book-detail', kwargs={'pk': self.object.pk})

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = '{} - edit'.format(self.object.title)
        return context

    def form_valid(self, form):
        response = super().form_valid(form)
        files = self.request.FILES.getlist('files')
        for f in files:
            ext = mimetypes.guess_extension(f.content_type)
            size = f.size

            old_file = File.objects.filter(book=self.object, extension=ext).first()
            if old_file:
                default_storage.delete(old_file.uuid.hex)
                old_file.delete()

            new_file = File(book=self.object,
                            extension=ext,
                            size=size,
                            uploader=self.request.user)
            new_file.save()
            default_storage.save(new_file.uuid.hex, f)

        return response


class AuthorListView(ListView):
    model = Author
    template_name = 'author_list.html'
    context_object_name = 'authors'
    extra_context = {'title': 'Author List'}


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
    extra_context = {'title': 'Tag List'}


class TagDetailView(DetailView):
    model = Tag
    template_name = 'tag_detail.html'
    context_object_name = 'tag'
    paginate_by = settings.ITEMS_PER_PAGE

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Tag {} - detail'.format(self.object.name)
        return context


class SeriesListView(ListView):
    model = Series
    template_name = 'series_list.html'
    context_object_name = 'series'
    extra_context = {'title': 'Series list'}


class SeriesDetailView(DetailView):
    model = Author
    template_name = 'series_detail.html'
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
    extra_context = {'title': 'Publisher list'}


class PublisherDetailView(DetailView):
    model = Publisher
    template_name = 'publisher_detail.html'
    context_object_name = 'publisher'
    paginate_by = settings.ITEMS_PER_PAGE

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Publisher "{}" - detail'.format(self.object.name)
        return context


class FileUploadView(FormView):
    form_class = FileUploadForm

    def form_valid(self, form):
        files = self.request.FILES.getlist('files')
        book = Book()
        book.save()
        for file in files:
            ext = mimetypes.guess_extension(file.content_type)
            size = file.size
            f = File(book=book,
                     extension=ext,
                     size=size,
                     uploader=self.request.user)
            f.save()
            default_storage.save(f.uuid.hex, file)
        return redirect(reverse('book-edit', kwargs={'pk': book.pk}))

    def form_invalid(self, form):
        from_uri = self.request.META['HTTP_REFERER']
        return redirect(from_uri)


class FileDownloadView(DetailView):
    model = File

    def get(self, request, pk):
        file = self.get_object()
        response = HttpResponse(default_storage.open(file.uuid.hex).read(),
                                content_type=mimetypes.guess_type(file.extension))
        filename = get_valid_filename(file.book.title + file.extension)
        response['Content-Disposition'] = 'attachment; filename=' + filename
        return response


class FileDeleteView(DetailView):
    model = File

    def get(self, request, pk):
        file = self.get_object()
        book_id = file.book.id
        default_storage.delete(file.uuid.hex)
        file.delete()
        redirect_uri = self.request.META.get('HTTP_REFERER', None) or reverse('book-edit', kwargs={'pk': book_id})
        return redirect(redirect_uri)


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



