from django.test import TestCase
from django.shortcuts import reverse
from .models import *
from mixer.backend.django import Mixer


class ListViewTestMixin:
    model = None
    context_object_name = None
    numbers_of_objects = 30
    object_per_page = 20
    is_paginated = True
    path_name = None
    path_url = None
    template_path = None

    @classmethod
    def setUpTestData(cls):
        mixer = Mixer(commit=False)
        objects = mixer.cycle(30).blend(cls.model)
        cls.model.objects.bulk_create(objects)

    def test_parameters(self):
        self.assertTrue(self.model)
        self.assertTrue(self.context_object_name)
        self.assertTrue(self.numbers_of_objects)
        self.assertTrue(self.path_name)
        self.assertTrue(self.path_url)

    def test_view_url_exists_at_desired_location(self):
        resp = self.client.get(self.path_url)
        self.assertEqual(resp.status_code, 200)

    def test_view_url_accessible_by_name(self):
        resp = self.client.get(reverse(self.path_name))
        self.assertEqual(resp.status_code, 200)

    def test_view_url_matching_with_name(self):
        url = reverse(self.path_name)
        self.assertEqual(url, self.path_url)

    def test_view_uses_correct_template(self):
        resp = self.client.get(reverse(self.path_name))
        self.assertEqual(resp.status_code, 200)
        self.assertTemplateUsed(resp, self.template_path)

    def test_pagination(self):
        resp = self.client.get(reverse(self.path_name))
        self.assertEqual(resp.status_code, 200)
        self.assertTrue('is_paginated' in resp.context)
        self.assertEqual(resp.context['is_paginated'], self.is_paginated)
        if self.is_paginated:
            self.assertTrue(len(resp.context[self.context_object_name]) == self.object_per_page)

    def test_lists_all_objects(self):
        resp = self.client.get(reverse(self.path_name) + '?page=2')
        self.assertEqual(resp.status_code, 200)
        self.assertTrue('is_paginated' in resp.context)
        self.assertEqual(resp.context['is_paginated'], self.is_paginated)
        number_of_objects = self.numbers_of_objects - self.object_per_page
        self.assertEqual(len(resp.context[self.context_object_name]), number_of_objects)

    @classmethod
    def tearDownTestData(cls):
        super().tearDownTestData()


class BookListViewTest(ListViewTestMixin, TestCase):
    __test__ = True
    model = Book
    context_object_name = 'books'
    path_name = "index"
    path_url = "/"
    is_paginated = True
    template_path = 'book_list.html'


class AuthorListViewTest(ListViewTestMixin, TestCase):
    __test__ = True
    model = Author
    context_object_name = 'authors'
    path_name = "author-list"
    path_url = "/authors"
    template_path = 'author_list.html'
    is_paginated = False
    object_per_page = 0


class TagListViewTest(ListViewTestMixin, TestCase):
    __test__ = True
    model = Tag
    context_object_name = 'tags'
    path_name = "tag-list"
    path_url = "/tags"
    template_path = 'tag_list.html'
    is_paginated = False
    object_per_page = 0


class SeriesListViewTest(ListViewTestMixin, TestCase):
    __test__ = True
    model = Series
    context_object_name = 'series'
    path_name = "series-list"
    path_url = "/series"
    template_path = 'series_list.html'
    is_paginated = False
    object_per_page = 0


class PublisherListViewTest(ListViewTestMixin, TestCase):
    __test__ = True
    model = Publisher
    context_object_name = 'publishers'
    path_name = "publisher-list"
    path_url = "/publishers"
    template_path = 'publisher_list.html'
    is_paginated = False
    object_per_page = 0


class DetailViewTestMixin:
    model = None
    path_url = None
    path_name = None
    template_path = None
    context_object_name = None

    @classmethod
    def setUpTestData(cls):
        mixer = Mixer()
        mixer.blend(cls.model)

    def test_view_url_exists_at_desired_location(self):
        resp = self.client.get(self.path_url)
        self.assertEqual(resp.status_code, 200)

    def test_view_url_accessible_by_name(self):
        resp = self.client.get(reverse(self.path_name, kwargs={'pk': 1}))
        self.assertEqual(resp.status_code, 200)

    def test_view_uses_correct_template(self):
        resp = self.client.get(reverse(self.path_name, kwargs={'pk': 1}))
        self.assertEqual(resp.status_code, 200)
        self.assertTemplateUsed(resp, self.template_path)

    def test_view_url_matching_with_name(self):
        url = reverse(self.path_name, kwargs={'pk': 1})
        self.assertEqual(url, self.path_url)

    def test_object(self):
        resp = self.client.get(reverse(self.path_name, kwargs={'pk': 1}))
        self.assertEqual(resp.status_code, 200)
        self.assertTrue(resp.context.get(self.context_object_name, False))


class BookDetailTest(DetailViewTestMixin, TestCase):
    model = Book
    path_url = '/book/1'
    path_name = 'book-detail'
    template_path = 'book_detail.html'
    context_object_name = 'book'


class AuthorDetailTest(DetailViewTestMixin, TestCase):
    model = Author
    path_url = '/author/1'
    path_name = 'author-detail'
    template_path = 'author_detail.html'
    context_object_name = 'author'


class TagDetailTest(DetailViewTestMixin, TestCase):
    model = Tag
    path_url = '/tag/1'
    path_name = 'tag-detail'
    template_path = 'tag_detail.html'
    context_object_name = 'tag'


class SeriesDetailTest(DetailViewTestMixin, TestCase):
    model = Series
    path_url = '/series/1'
    path_name = 'series-detail'
    template_path = 'series_detail.html'
    context_object_name = 'series'


class PublisherDetailTest(DetailViewTestMixin, TestCase):
    model = Publisher
    path_url = '/publisher/1'
    path_name = 'publisher-detail'
    template_path = 'publisher_detail.html'
    context_object_name = 'publisher'


class SearchViewTest(TestCase):
    invalid_queries = [
        ('qq', 'Query must have min 3 character!'),
        (':books', 'Wrong search operator!'),
    ]
    valid_queries = [
        ('query', reverse('book-search') + "?query=query"),
        ('  query', reverse('book-search') + "?query=query"),
        ('book:query', reverse('book-search') + "?query=query"),
        ('book:   query', reverse('book-search') + "?query=query"),
        # ('author: query', reverse('author-search') + "?query=query"),
    ]
    path_url = '/search?query={}'

    def test_invalid_query(self):
        for query in self.invalid_queries:
            resp = self.client.get(self.path_url.format(query[0]))
            self.assertWarnsMessage(resp, query[1])
            self.assertRedirects(resp, reverse('index'))

    def test_valid_query(self):
        import urllib.parse as urlparse

        for query in self.valid_queries:
            resp = self.client.get(self.path_url.format(query[0]))
            search_arg = (urlparse.parse_qs(urlparse.urlparse(resp.url).query)['query'])[0]
            self.assertEqual(search_arg, 'query')
            self.assertRedirects(resp, query[1])
