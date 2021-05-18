from django.test import TestCase
from django.shortcuts import reverse
from django.contrib.auth import get_user_model
from .models import *
from mixer.backend.django import Mixer


class ListViewTestMixin:
    model = None
    context_object_name = None
    numbers_of_objects = 30
    object_per_page = 20
    is_paginated = True
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
        ('author:query', reverse('author-search') + "?query=query"),
        ('author:   query', reverse('author-search') + "?query=query"),
        ('tag:query', reverse('tag-search') + "?query=query"),
        ('tag:   query', reverse('tag-search') + "?query=query"),
        ('series:query', reverse('series-search') + "?query=query"),
        ('series:   query', reverse('series-search') + "?query=query"),
        ('publisher:query', reverse('publishers-search') + "?query=query"),
        ('publisher:   query', reverse('publishers-search') + "?query=query"),
    ]
    default_status = 302
    path_url = '/search'
    path_name = 'search'

    def test_view_url_exists_at_desired_location(self):
        resp = self.client.get(self.path_url)
        self.assertEqual(resp.status_code, 302)

    def test_view_url_accessible_by_name(self):
        resp = self.client.get(reverse(self.path_name))
        self.assertEqual(resp.status_code, 302)

    def test_view_url_matching_with_name(self):
        url = reverse(self.path_name)
        self.assertEqual(url, self.path_url)

    def test_invalid_query(self):
        for query in self.invalid_queries:
            resp = self.client.get(self.path_url + '?query={}'.format(query[0]))
            self.assertEqual(resp.status_code, self.default_status)
            self.assertWarnsMessage(resp, query[1])
            self.assertRedirects(resp, reverse('index'))

    def test_valid_query(self):
        import urllib.parse as urlparse

        for query in self.valid_queries:
            resp = self.client.get(self.path_url + '?query={}'.format(query[0]))
            self.assertEqual(resp.status_code, self.default_status)
            self.assertRedirects(resp, query[1])
            search_arg = (urlparse.parse_qs(urlparse.urlparse(resp.url).query)['query'])[0]
            self.assertEqual(search_arg, 'query')


class SubjectSearchViewTestMixin:
    model = None
    path_url = None
    path_name = None
    context_object_name = 'object'
    invalid_query = 'qq'
    valid_query = 'query'
    search_attribute = None
    numbers_of_objects = 50

    @classmethod
    def setUpTestData(cls):
        mixer = Mixer(commit=False)
        objects = []
        for i in range(cls.numbers_of_objects):
            object = mixer.blend(cls.model)
            object.__setattr__(cls.search_attribute, cls.valid_query + str(i))
            objects.append(object)
        cls.model.objects.bulk_create(objects)

    def test_view_url_exists_at_desired_location(self):
        resp = self.client.get(self.path_url)
        self.assertEqual(resp.status_code, 302)

    def test_view_url_accessible_by_name(self):
        resp = self.client.get(reverse(self.path_name))
        self.assertEqual(resp.status_code, 302)

    def test_view_url_matching_with_name(self):
        url = reverse(self.path_name)
        self.assertEqual(url, self.path_url)

    def test_invalid_query(self):
        resp = self.client.get(self.path_url + '?query=' + self.invalid_query)
        self.assertWarnsMessage(resp, 'Query must have min 3 character!')
        self.assertRedirects(resp, reverse('index'))

    def test_valid_query(self):
        resp = self.client.get(self.path_url + '?query=' + self.valid_query)
        self.assertEqual(resp.status_code, 200)

    def test_valid_multiple_result_search(self):
        resp = self.client.get(self.path_url + '?query=' + self.valid_query)
        self.assertEquals(len(resp.context[self.context_object_name]), 20)

    def test_valid_multiple_result_pagination(self):
        resp = self.client.get(self.path_url + '?query=' + self.valid_query)
        self.assertEquals(resp.context['page_obj'].paginator.num_pages, 3)

    def test_valid_single_result_search(self):
        resp = self.client.get(self.path_url + '?query=query49')
        self.assertEquals(len(resp.context[self.context_object_name]), 1)


class BookSearchViewTest(SubjectSearchViewTestMixin, TestCase):
    model = Book
    invalid_query = 'qq'
    valid_query = 'query'
    path_url = '/books/search'
    path_name = 'book-search'
    search_attribute = 'title'
    context_object_name = 'books'


class AuthorSearchViewTest(SubjectSearchViewTestMixin, TestCase):
    model = Author
    invalid_query = 'qq'
    valid_query = 'query'
    path_url = '/authors/search'
    path_name = 'author-search'
    search_attribute = 'name'
    context_object_name = 'authors'


class TagsSearchViewTest(SubjectSearchViewTestMixin, TestCase):
    model = Tag
    invalid_query = 'qq'
    valid_query = 'query'
    path_url = '/tags/search'
    path_name = 'tag-search'
    search_attribute = 'name'
    context_object_name = 'tags'


class SeriesSearchViewTest(SubjectSearchViewTestMixin, TestCase):
    model = Series
    invalid_query = 'qq'
    valid_query = 'query'
    path_url = '/series/search'
    path_name = 'series-search'
    search_attribute = 'title'
    context_object_name = 'series'


class PublisherSearchViewTest(SubjectSearchViewTestMixin, TestCase):
    model = Publisher
    invalid_query = 'qq'
    valid_query = 'query'
    path_url = '/publishers/search'
    path_name = 'publishers-search'
    search_attribute = 'name'
    context_object_name = 'publishers'


class SubjectCreateViewTestMixin:
    model = None
    path_url = None
    path_name = None
    success_url = None
    template_path = None
    valid_data = {}
    invalid_data = {}

    @classmethod
    def setUpTestData(cls):
        get_user_model().objects.create_user('temporary', 'temporary@temp.com', 'temporary')

    def test_view_url_exists_at_desired_location(self):
        self.client.login(username='temporary', password='temporary')
        resp = self.client.get(self.path_url)
        self.assertEqual(resp.status_code, 200)

    def test_view_url_accessible_by_name(self):
        self.client.login(username='temporary', password='temporary')
        resp = self.client.get(reverse(self.path_name))
        self.assertEqual(resp.status_code, 200)

    def test_view_url_matching_with_name(self):
        url = reverse(self.path_name)
        self.assertEqual(url, self.path_url)

    def test_template(self):
        self.client.login(username='temporary', password='temporary')
        resp = self.client.get(reverse(self.path_name))
        self.assertTemplateUsed(resp, self.template_path)

    def test_valid_form(self):
        self.client.login(username='temporary', password='temporary')
        for num, data in enumerate(self.valid_data, start=1):
            resp = self.client.post(self.path_url, data=data)
            self.assertEqual(resp.status_code, 302)
            self.assertRedirects(resp, self.success_url.format(num))

    def test_invalid_form(self):
        self.client.login(username='temporary', password='temporary')
        resp = self.client.post(self.path_url, data=self.invalid_data)
        self.assertEqual(resp.status_code, 200)
        for key in self.valid_data[-1].keys():
            self.assertFormError(resp, 'form', key, 'Это поле не может быть пустым.')

    def test_without_auth(self):
        resp = self.client.post(self.path_url)
        self.assertEqual(resp.status_code, 302)
        resp = self.client.get(self.path_url)
        self.assertEqual(resp.status_code, 302)


class AuthorCreateViewTest(SubjectCreateViewTestMixin, TestCase):
    model = Author
    path_url = '/authors/add'
    path_name = 'author-create'
    success_url = '/author/{}'
    template_path = 'author_form.html'
    valid_data = [
        {'name': 'Test Author', 'link': 'empty', 'description': 'aaa'},
        {'name': 'Test Author', 'link': 'empty'},
        {'name': 'Test Author'}
    ]
    invalid_data = {}


class TagCreateViewTest(SubjectCreateViewTestMixin, TestCase):
    model = Tag
    path_url = '/tags/add'
    path_name = 'tag-create'
    success_url = '/tag/{}'
    template_path = 'tag_form.html'
    valid_data = [{'name': 'Test Tag'}]
    invalid_data = {}


class SeriesCreateViewTest(SubjectCreateViewTestMixin, TestCase):
    model = Series
    path_url = '/series/add'
    path_name = 'series-create'
    success_url = '/series/{}'
    template_path = 'series_form.html'
    valid_data = [
        {'title': 'Test Author', 'description': 'aaa'},
        {'title': 'Test Author'}
    ]
    invalid_data = {}


class PublisherCreateViewTest(SubjectCreateViewTestMixin, TestCase):
    model = Publisher
    path_url = '/publishers/add'
    path_name = 'publisher-create'
    success_url = '/publisher/{}'
    template_path = 'publisher_form.html'
    valid_data = [
        {'name': 'Test Publisher', 'link': 'empty'},
        {'name': 'Test Publisher'}
    ]
    invalid_data = {}


class SubjectDeleteViewTestMixin:
    model = None
    path_url = None
    path_name = None
    subject_url = None
    success_url = None

    def setUp(self):
        mixer = Mixer()
        mixer.blend(self.model)
        get_user_model().objects.create_user('temporary', 'temporary@temp.com', 'temporary')

    def test_view_url_matching_with_name(self):
        url = reverse(self.path_name, kwargs={'pk': 1})
        self.assertEqual(url, self.path_url)

    def test_object_on_exist(self):
        resp = self.client.get(self.subject_url)
        self.assertEqual(resp.status_code, 200)

    def test_object_delete(self):
        self.client.login(username='temporary', password='temporary')
        resp = self.client.get(self.path_url)
        self.assertEqual(resp.status_code, 302)
        self.assertRedirects(resp, self.success_url)
        resp = self.client.get(self.subject_url)
        self.assertEqual(resp.status_code, 404)


class AuthorDeleteViewTest(SubjectDeleteViewTestMixin, TestCase):
    model = Author
    path_url = '/author/1/delete'
    path_name = 'author-delete'
    subject_url = '/author/1'
    success_url = '/authors'


class TagDeleteViewTest(SubjectDeleteViewTestMixin, TestCase):
    model = Tag
    path_url = '/tag/1/delete'
    path_name = 'tag-delete'
    subject_url = '/tag/1'
    success_url = '/tags'


class SeriesDeleteViewTest(SubjectDeleteViewTestMixin, TestCase):
    model = Series
    path_url = '/series/1/delete'
    path_name = 'series-delete'
    subject_url = '/series/1'
    success_url = '/series'


class PublisherDeleteViewTest(SubjectDeleteViewTestMixin, TestCase):
    model = Publisher
    path_url = '/publisher/1/delete'
    path_name = 'publisher-delete'
    subject_url = '/publisher/1'
    success_url = '/publishers'
    

class SubjectEditViewTestMixin(SubjectCreateViewTestMixin):
    model = None
    path_url = None
    path_name = None
    success_url = None
    template_path = None
    valid_data = {}
    invalid_data = {}

    @classmethod
    def setUpTestData(cls):
        mixer = Mixer()
        mixer.blend(cls.model)
        get_user_model().objects.create_user('temporary', 'temporary@temp.com', 'temporary')

    def test_view_url_exists_at_desired_location(self):
        self.client.login(username='temporary', password='temporary')
        resp = self.client.get(self.path_url)
        self.assertEqual(resp.status_code, 200)

    def test_view_url_accessible_by_name(self):
        self.client.login(username='temporary', password='temporary')
        resp = self.client.get(reverse(self.path_name, kwargs={'pk': 1}))
        self.assertEqual(resp.status_code, 200)

    def test_view_url_matching_with_name(self):
        url = reverse(self.path_name, kwargs={'pk': 1})
        self.assertEqual(url, self.path_url)

    def test_template(self):
        self.client.login(username='temporary', password='temporary')
        resp = self.client.get(reverse(self.path_name, kwargs={'pk': 1}))
        self.assertTemplateUsed(resp, self.template_path)

    def test_valid_form(self):
        self.client.login(username='temporary', password='temporary')
        for data in self.valid_data:
            resp = self.client.post(self.path_url, data=data)
            self.assertEqual(resp.status_code, 302)
            self.assertRedirects(resp, self.success_url.format(1))

    def test_invalid_form(self):
        self.client.login(username='temporary', password='temporary')
        resp = self.client.post(self.path_url, data=self.invalid_data)
        self.assertEqual(resp.status_code, 200)
        for key in self.valid_data[-1].keys():
            self.assertFormError(resp, 'form', key, 'Это поле не может быть пустым.')

    def test_without_auth(self):
        resp = self.client.post(self.path_url)
        self.assertEqual(resp.status_code, 302)
        resp = self.client.get(self.path_url)
        self.assertEqual(resp.status_code, 302)


class AuthorEditViewTest(SubjectEditViewTestMixin, TestCase):
    model = Author
    path_url = '/author/1/edit'
    path_name = 'author-edit'
    success_url = '/author/1'
    template_path = 'author_form.html'
    valid_data = [
        {'name': 'Test Author', 'link': 'empty', 'description': 'aaa'},
        {'name': 'Test Author', 'link': 'empty'},
        {'name': 'Test Author'}
    ]
    invalid_data = {}


class TagEditViewTest(SubjectEditViewTestMixin, TestCase):
    model = Tag
    path_url = '/tag/1/edit'
    path_name = 'tag-edit'
    success_url = '/tag/{}'
    template_path = 'tag_form.html'
    valid_data = [{'name': 'Test Tag'}]
    invalid_data = {}


class SeriesEditViewTest(SubjectEditViewTestMixin, TestCase):
    model = Series
    path_url = '/series/1/edit'
    path_name = 'series-edit'
    success_url = '/series/{}'
    template_path = 'series_form.html'
    valid_data = [
        {'title': 'Test Author', 'description': 'aaa'},
        {'title': 'Test Author'}
    ]
    invalid_data = {}


class PublisherEditViewTest(SubjectEditViewTestMixin, TestCase):
    model = Publisher
    path_url = '/publisher/1/edit'
    path_name = 'publisher-edit'
    success_url = '/publisher/{}'
    template_path = 'publisher_form.html'
    valid_data = [
        {'name': 'Test Publisher', 'link': 'empty'},
        {'name': 'Test Publisher'}
    ]
    invalid_data = {}
