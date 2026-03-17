import django_filters
from .models import Idea


class IdeaFilter(django_filters.FilterSet):
    category = django_filters.CharFilter()
    creator = django_filters.NumberFilter(field_name='creator__id')

    class Meta:
        model = Idea
        fields = ['category', 'creator']
