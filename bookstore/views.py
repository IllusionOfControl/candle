from _ast import Or

from django.shortcuts import render, redirect, reverse
from django.http import Http404, HttpResponse
from django.core.files.storage import default_storage
from django.utils.text import get_valid_filename
from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic.base import View
from django.views.generic.list import ListView
from django.views.generic.edit import CreateView, UpdateView, DeleteView, FormView
from django.views.generic.detail import DetailView
from django.conf import settings
from django.urls import reverse_lazy
from django.core.paginator import Paginator
from django.db.models import Count
from bookstore.models import *
from bookstore.forms import BookForm, FileUploadForm
import mimetypes


class OrderingMixin:
    queryset = None
    order_by_default = 'name'

    def get_queryset(self):
        self.queryset = self.model.objects.annotate(book_nums=Count('books'))
        return super().get_queryset()

    def get_ordering(self):
        ordering = self.request.GET.get('ordering', self.order_by_default)
        return ordering


class BookListView(ListView):
    model = Book
    template_name = 'book_list.html'
    paginate_by = settings.ITEMS_PER_PAGE
    extra_context = {'title': 'Book list'}
    context_object_name = 'books'

    def get_ordering(self):
        ordering = self.request.GET.get('ordering', '-created_at')
        return ordering


class BookDetailView(DetailView):
    model = Book
    template_name = 'book_detail.html'
    context_object_name = 'book'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = '{} - detail'.format(self.object.title)
        return context


class BookEditView(LoginRequiredMixin, UpdateView):
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
        from pathlib import Path

        response = super().form_valid(form)
        files = self.request.FILES.getlist('files')
        cover = self.request.FILES.get('cover', None)
        if cover:
            self.object.has_cover = True
            self.object.save()
            if default_storage.exists("covers/" + self.object.uuid.hex):
                default_storage.delete("covers/" + self.object.uuid.hex)
            default_storage.save("covers/" + self.object.uuid.hex, cover)
        for f in files:
            ext = Path(f.name).suffix[1:].lower()
            size = f.size

            old_file = File.objects.filter(book=self.object, extension=ext).first()
            if old_file:
                default_storage.delete('books/' + old_file.uuid.hex)
                old_file.delete()

            new_file = File(book=self.object,
                            extension=ext,
                            size=size,
                            uploader=self.request.user)
            new_file.save()
            default_storage.save('books/' + new_file.uuid.hex, f)

        return response


class BookDeleteView(LoginRequiredMixin, DeleteView):
    model = Book
    success_url = reverse_lazy('book-list')

    def get(self, *args, **kwargs):
        return self.post(*args, **kwargs)


class AuthorListView(OrderingMixin, ListView):
    model = Author
    template_name = 'author_list.html'
    context_object_name = 'authors'
    extra_context = {'title': 'Author List'}


class AuthorDetailView(DetailView):
    model = Author
    template_name = 'author_detail.html'
    context_object_name = 'author'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Author {} - detail'.format(self.object.name)
        books = self.object.books.all()
        paginator = Paginator(books, settings.ITEMS_PER_PAGE)
        page_number = self.request.GET.get('page')
        context['books'] = books
        context['page_obj'] = paginator.get_page(page_number)
        return context


class AuthorCreateView(LoginRequiredMixin, CreateView):
    model = Author
    fields = ['name', 'link', 'description']
    template_name = 'author_form.html'

    def get_form(self, form_class=None):
        form = super().get_form(form_class)
        form.fields['link'].required = False
        form.fields['description'].required = False
        return form

    def get_success_url(self):
        return reverse('author-detail', kwargs={'pk': self.object.pk})


class AuthorEditView(LoginRequiredMixin, UpdateView):
    model = Author
    fields = ['name', 'link', 'description']
    template_name = 'author_form.html'
    context_object_name = 'author'

    def get_form(self, form_class=None):
        form = super().get_form(form_class)
        form.fields['link'].required = False
        form.fields['description'].required = False
        return form

    def get_success_url(self):
        return reverse('author-detail', kwargs={'pk': self.object.pk})

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Author {} - edit'.format(self.object.name)
        return context


class AuthorDeleteView(LoginRequiredMixin, DeleteView):
    model = Author
    success_url = reverse_lazy('author-list')

    def get(self, *args, **kwargs):
        return self.post(*args, **kwargs)


class TagListView(OrderingMixin, ListView):
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
        books = self.object.books.all()
        paginator = Paginator(books, settings.ITEMS_PER_PAGE)
        page_number = self.request.GET.get('page')
        context['page_obj'] = paginator.get_page(page_number)
        return context


class TagCreateView(LoginRequiredMixin, CreateView):
    model = Tag
    fields = ['name']
    template_name = 'tag_form.html'

    def get_success_url(self):
        return reverse('tag-detail', kwargs={'pk': self.object.pk})


class TagEditView(LoginRequiredMixin, UpdateView):
    model = Tag
    fields = ['name']
    template_name = 'tag_form.html'
    context_object_name = 'tag'

    def get_success_url(self):
        return reverse('tag-detail', kwargs={'pk': self.object.pk})

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Tag {} - edit'.format(self.object.name)
        return context


class TagDeleteView(LoginRequiredMixin, DeleteView):
    model = Tag
    success_url = reverse_lazy('tag-list')

    def get(self, *args, **kwargs):
        return self.post(*args, **kwargs)


class SeriesListView(OrderingMixin, ListView):
    model = Series
    template_name = 'series_list.html'
    context_object_name = 'series'
    extra_context = {'title': 'Series list'}
    order_by_default = 'title'


class SeriesDetailView(DetailView):
    model = Series
    template_name = 'series_detail.html'
    context_object_name = 'series'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Book series "{}" - detail'.format(self.object.title)
        books = self.object.books.all()
        paginator = Paginator(books, settings.ITEMS_PER_PAGE)
        page_number = self.request.GET.get('page')
        context['page_obj'] = paginator.get_page(page_number)
        return context


class SeriesCreateView(LoginRequiredMixin, CreateView):
    model = Series
    fields = ['title']
    template_name = 'series_form.html'

    def get_success_url(self):
        return reverse('series-detail', kwargs={'pk': self.object.pk})


class SeriesEditView(LoginRequiredMixin, UpdateView):
    model = Series
    fields = ['title', 'description']
    template_name = 'series_form.html'
    context_object_name = 'tag'

    def get_form(self, form_class=None):
        form = super().get_form(form_class)
        form.fields['description'].required = False
        return form

    def get_success_url(self):
        return reverse('series-detail', kwargs={'pk': self.object.pk})

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Book series {} - edit'.format(self.object.title)
        return context


class SeriesDeleteView(LoginRequiredMixin, DeleteView):
    model = Series
    success_url = reverse_lazy('series-list')

    def get(self, *args, **kwargs):
        return self.post(*args, **kwargs)


class PublisherListView(OrderingMixin, ListView):
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
        books = self.object.books.all()
        paginator = Paginator(books, settings.ITEMS_PER_PAGE)
        page_number = self.request.GET.get('page')
        context['page_obj'] = paginator.get_page(page_number)
        return context


class PublisherCreateView(LoginRequiredMixin, CreateView):
    model = Publisher
    fields = ['name', 'link']
    template_name = 'publisher_form.html'

    def get_form(self, form_class=None):
        form = super().get_form(form_class)
        form.fields['link'].required = False
        return form

    def get_success_url(self):
        return reverse('publisher-detail', kwargs={'pk': self.object.pk})


class PublisherEditView(LoginRequiredMixin, UpdateView):
    model = Publisher
    fields = ['name', 'link']
    template_name = 'publisher_form.html'
    context_object_name = 'publisher'

    def get_form(self, form_class=None):
        form = super().get_form(form_class)
        form.fields['link'].required = False
        return form

    def get_success_url(self):
        return reverse('publisher-detail', kwargs={'pk': self.object.pk})

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Publisher {} - edit'.format(self.object.name)
        return context


class PublisherDeleteView(LoginRequiredMixin, DeleteView):
    model = Publisher
    success_url = reverse_lazy('publisher-list')

    def get(self, *args, **kwargs):
        return self.post(*args, **kwargs)


class FileUploadView(LoginRequiredMixin, FormView):
    form_class = FileUploadForm

    def form_valid(self, form):
        from pathlib import Path

        files = self.request.FILES.getlist('files')
        book = Book()
        book.save()

        for file in files:
            ext = Path(file.name).suffix[1:].lower()
            size = file.size
            f = File(book=book,
                     extension=ext,
                     size=size,
                     uploader=self.request.user)
            f.save()
            default_storage.save("books/" + f.uuid.hex, file)
        return redirect(reverse('book-edit', kwargs={'pk': book.pk}))

    def form_invalid(self, form):
        print(form.errors)
        redirect_url = self.request.META.get('HTTP_REFERER', reverse('index'))
        return redirect(redirect_url)

    def get(self, request):
        redirect_url = self.request.META.get('HTTP_REFERER', reverse('index'))
        return redirect(redirect_url)


class FileDownloadView(DetailView):
    model = File

    def get(self, request, *args, **kwargs):
        file = self.get_object()
        response = HttpResponse(default_storage.open("books/" + file.uuid.hex).read(),
                                content_type=mimetypes.guess_type(file.extension))
        filename = get_valid_filename(file.book.title + '.' + file.extension)
        response['Content-Disposition'] = 'attachment; filename=' + filename
        return response


class FileDeleteView(LoginRequiredMixin, DetailView):
    model = File

    def get(self, request, *args, **kwargs):
        file = self.get_object()
        book_id = file.book.id
        default_storage.delete(file.uuid.hex)
        file.delete()
        redirect_uri = self.request.META.get('HTTP_REFERER', None) or reverse('book-edit', kwargs={'pk': book_id})
        return redirect(redirect_uri)


class BookCoverView(DetailView):
    model = Book

    def get(self, request, *args, **kwargs):
        book = self.get_object()
        response = HttpResponse(default_storage.open('covers/' + book.uuid.hex).read(),
                                content_type='image/jpeg')
        response['Content-Disposition'] = 'attachment'
        return response


class StatisticView(View):
    def get(self, request, *args, **kwargs):
        context = {
            'book_count': Book.objects.count(),
            'author_count': Author.objects.count(),
            'tag_count': Tag.objects.count(),
            'series_count': Series.objects.count(),
            'publisher_count': Publisher.objects.count()
        }
        return render(request=request, template_name='statistic.html', context=context)


class SearchView(View):
    def get(self, request, *args, **kwargs):
        import re
        query_string = self.request.GET.get('query', '')
        query_subject = None
        query = re.match(r'(^\w*:)(.*)', query_string)

        if query:
            query_subject = query.group(1)
            query_string = query.group(2)

        query_string = re.match(r'\s*(.*)', query_string).group(1)

        if len(query_string) < 3:
            messages.warning(self.request, 'Query must have min 3 character!')
            redirect_uri = self.request.META.get('HTTP_REFERER', reverse('index'))
            return redirect(redirect_uri)

        if query_subject:
            if query_subject == 'book:':
                return redirect(reverse('book-search') + "?query=" + query_string)
            elif query_subject == 'author:':
                return redirect(reverse('author-search') + "?query=" + query_string)
            elif query_subject == 'tag:':
                return redirect(reverse('tag-search') + "?query=" + query_string)
            elif query_subject == 'series:':
                return redirect(reverse('series-search') + "?query=" + query_string)
            elif query_subject == 'publisher:':
                return redirect(reverse('publishers-search') + "?query=" + query_string)
            else:
                messages.warning(self.request, 'Wrong search operator!')
                redirect_uri = self.request.META.get('HTTP_REFERER', reverse('index'))
                return redirect(redirect_uri)

        return redirect(reverse('book-search') + "?query=" + query_string)


class SubjectSearchView(ListView):
    template_name = 'search_page.html'
    paginate_by = 20

    def get_query_string(self):
        query_string = self.request.GET.get('query', '')
        return query_string

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Search by "{}"'.format(self.get_query_string())
        context['query_string'] = self.get_query_string()
        context['objects_count'] = self.get_queryset().count()
        context['search_object'] = self.context_object_name
        return context

    def get(self, request, *args, **kwargs):
        query_string = self.get_query_string()
        if len(query_string) < 3:
            messages.warning(self.request, 'Query must have min 3 character!')
            redirect_uri = self.request.META.get('HTTP_REFERER', reverse('index'))
            return redirect(redirect_uri)
        self.queryset = self.model.objects.search(query_string)
        return super().get(self.request, args, kwargs)


class BookSearchView(SubjectSearchView):
    model = Book
    context_object_name = 'books'


class AuthorSearchView(SubjectSearchView):
    model = Author
    context_object_name = 'authors'


class TagSearchView(SubjectSearchView):
    model = Tag
    context_object_name = 'tags'


class SeriesSearchView(SubjectSearchView):
    model = Series
    context_object_name = 'series'


class PublisherSearchView(SubjectSearchView):
    model = Publisher
    context_object_name = 'publishers'


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
