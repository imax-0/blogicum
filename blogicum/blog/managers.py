from django.db import models
from django.utils import timezone


class PostsManager(models.Manager):
    def get_queryset(self) -> models.QuerySet:
        return super().get_queryset().select_related(
            'author', 'category', 'location'
        ).filter(
            pub_date__lte=timezone.now(),
            is_published=True,
            category__is_published=True,
        )
