from rest_framework import serializers

from comments.models import Comment


class RecursiveSerializer(serializers.ModelSerializer):
    def to_representation(self, value):
        serializer = CommentSerializer(value, context=self.context)
        return serializer.data


class CommentSerializer(serializers.ModelSerializer):
    user = serializers.ReadOnlyField(source='user.email')
    replies = RecursiveSerializer(many=True, read_only=True)

    class Meta:
        model = Comment
        fields = (
            'id',
            'idea',
            'user',
            'text',
            'parent',
            'replies',
            'created_at'
        )
