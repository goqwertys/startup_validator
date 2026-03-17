from datetime import timedelta

from django.contrib import admin
from django.db.models import Sum
from django.db.models.functions import Coalesce
from django.utils import timezone

from ideas.models import Idea


class TopIdeasFilter(admin.SimpleListFilter):
    title = 'Top ideas'
    parameter_name = 'top'

    def lookups(self, request, model_admin):
        return (
            ('top', 'Top 10'),
            ('week', 'Top this week')
        )

    def queryset(self, request, queryset):
        queryset = queryset.annotate(score=Coalesce(Sum('votes__value'), 0))

        if self.value() == 'top':
            return queryset.order_by('-score')[:10]

        if self.value() == 'week':
            week_ago = timezone.now() - timedelta(days=7)
            return queryset.filter(created_at__gte=week_ago).order_by('-score')

        return queryset


@admin.register(Idea)
class IdeaAdmin(admin.ModelAdmin):

    list_display = ('id', 'title', 'creator', 'category', 'score', 'created_at')

    def get_queryset(self, request):
        qs = super().get_queryset(request)
        return qs.annotate(score=Coalesce(Sum('votes__value'), 0))

    def score(self, obj):
        return obj.score

    score.admin_order_field = 'score'

    list_filter = ('category', 'created_at', TopIdeasFilter)
    search_fields = ('title', 'description')
    ordering = ('-created_at',)