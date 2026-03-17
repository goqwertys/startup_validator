from django.contrib import admin
from django.db.models import Sum
from django.db.models.functions import Coalesce

from ideas.models import Idea


@admin.register(Idea)
class IdeaAdmin(admin.ModelAdmin):

    list_display = ('id', 'title', 'creator', 'category', 'score', 'created_at')

    def get_queryset(self, request):
        qs = super().get_queryset(request)
        return qs.annotate(score=Coalesce(Sum('votes__value'), 0))

    def score(self, obj):
        return obj.score

    score.admin_order_field = 'score'

    list_filter = ('category', 'created_at')
    search_fields = ('title', 'description')
    ordering = ('-created_at',)
