from rest_framework import serializers
from .models import Idea


class IdeaSerializer(serializers.ModelSerializer):

    creator = serializers.ReadOnlyField(source='creator.email')
    score = serializers.IntegerField(read_only=True)

    class Meta:
        model = Idea
        fields = (
            'id',
            'title',
            'description',
            'category',
            'creator',
            'score',
            'created_at'
        )
