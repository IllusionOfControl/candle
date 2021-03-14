from django.db import models
from django.db.models import Q


class BookManager(models.Manager):
    use_for_related_fields = True

    def search(self, query=None):
        queryset = self.get_queryset()
        if query:
            or_lookup = (Q(title__contains=query) | Q(description__contains=query))
            queryset = queryset.filter(or_lookup)

        return queryset
