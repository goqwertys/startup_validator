from django.contrib import admin

from ideas.models import Idea


@admin.register(Idea)
class IdeaAdmin(admin.ModelAdmin):

    list_display = ('id', 'title', 'category', 'creator', 'score', 'created_at')
    list_filter = ('category', 'created_at')
    search_fields = ('title', 'description')
    ordering = ('-created_at',)
