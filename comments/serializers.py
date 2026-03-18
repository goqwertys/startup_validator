from rest_framework import serializers

from comments.models import Comment


class CommentSerializer(serializers.ModelSerializer):
    users = serializers.ReadOnlyField(source='user.email')

    class Meta:
        model = Comment
        fields = ('id', 'idea', 'user', 'text', 'created_at')
