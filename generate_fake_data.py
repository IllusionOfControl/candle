import os
import random

os.environ["DJANGO_ALLOW_ASYNC_UNSAFE"] = "true"
os.environ["DJANGO_SETTINGS_MODULE"] = "candle.settings"

import django
django.setup()
from bookstore.models import *
from mixer.backend.django import Mixer


mixer = Mixer(commit=False)

MULTIPLIER = 1
AUTHOR_COUNT = MULTIPLIER * 5
PUBLISHER_COUNT = MULTIPLIER * 5
TAGS_COUNT = MULTIPLIER * 5
SERIES_COUNT = MULTIPLIER * 5
IDENTIFIERS_COUNT = MULTIPLIER * 30
BOOKS_COUNT = MULTIPLIER * 30


def generate_fields():
    print('Generating Authors')
    authors = mixer.cycle(AUTHOR_COUNT).blend(Author, name=mixer.faker.name)
    print('Generating Publishers')
    publishers = mixer.cycle(PUBLISHER_COUNT).blend(Publisher, name=mixer.faker.company)
    print('Generating Tags')
    tags = mixer.cycle(TAGS_COUNT).blend(Tag, name=mixer.faker.word)
    print('Generating Series')
    series = mixer.cycle(SERIES_COUNT).blend(Series, title=mixer.faker.sentence)

    Author.objects.bulk_create(authors)
    Publisher.objects.bulk_create(publishers)
    Tag.objects.bulk_create(tags)
    Series.objects.bulk_create(series)

    print('Updating models')
    authors = Author.objects.all()[:AUTHOR_COUNT]
    publishers = Publisher.objects.all()[:PUBLISHER_COUNT]
    tags = Tag.objects.all()[:TAGS_COUNT]
    series = Series.objects.all()[:SERIES_COUNT]

    print('Generating Books')
    books = mixer.cycle(BOOKS_COUNT).blend(Book, title=mixer.faker.sentence, user=mixer.SELECT, publisher=mixer.SELECT,
                                           series=mixer.SELECT)
    Book.objects.bulk_create(books)
    books = Book.objects.all()[:BOOKS_COUNT]

    for book in books:
        book.authors.add(random.choice(authors))
        book.tags.add(random.choice(tags))
        book.save()


if __name__ == '__main__':
    generate_fields()
