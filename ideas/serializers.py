from rest_framework import serializers
from .models import Idea


class IdeaSerializer(serializers.ModelSerializer):

    creator = serializers.ReadOnlyField(source='creator.email')

    class Meta:
        model = Idea
        fields = (
            'id',
            'title',
            'description',
            'category',
            'creator',
            'created_at'
        )
