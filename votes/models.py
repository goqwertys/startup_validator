from django.conf import settings
from django.db import models


class Vote(models.Model):

    class VoteType(models.IntegerChoices):
        UP = 1, 'Upvote',
        DOWN = -1, 'Downvote'

    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='votes'
    )

    idea = models.ForeignKey(
        'ideas.Idea',
        on_delete=models.CASCADE,
        related_name='votes'
    )

    value = models.SmallIntegerField(choices=VoteType.choices)

    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=['user', 'idea'],
                name='unique_user_idea_vote'
            )
        ]

    def __str__(self):
        return f'{self.user} -> {self.idea} ({self.value})'
