from datetime import timedelta

from django.utils import timezone

import django_filters
from .models import Idea


class IdeaFilter(django_filters.FilterSet):
    category = django_filters.CharFilter()
    creator = django_filters.NumberFilter(field_name='creator__id')

    period = django_filters.CharFilter(method='filter_period')

    def filter_period(self, queryset, name, value):

        if value == 'week':
            week_ago = timezone.now() - timedelta(days=7)
            return queryset.filter(created_at__gte=week_ago)

        if value == 'deay':
            day_ago = timezone.now() - timedelta(days=1)
            return queryset.filter(created_at__gte=day_ago)

        return queryset

    class Meta:
        model = Idea
        fields = ['category', 'creator']
