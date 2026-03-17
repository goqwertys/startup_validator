from rest_framework import serializers

from votes.models import Vote


class VoteSerializer(serializers.ModelSerializer):
    class Meta:
        model = Vote
        fields = ('id', 'idea', 'value')

    def create(self, validated_data):
        user = self.context['request'].user
        idea = validated_data['idea']
        value = validated_data['value']

        vote, created = Vote.objects.update_or_create(
            user=user,
            idea=idea,
            defaults={'value': value}
        )
        return vote
