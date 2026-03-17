from django.conf import settings
from django.db import models
from django.db.models import Sum


class Idea(models.Model):

    class Category(models.TextChoices):
        TECH = "tech", "Tech"
        AI = "ai", "AI"
        FINANCE = "finance", "Finance"
        EDUCATION = "education", "Education"
        OTHER = "other", "Other"

    title = models.CharField(max_length=255)
    description = models.TextField()
    category = models.CharField(
        max_length=50,
        choices=Category.choices,
        default=Category.OTHER
    )

    creator = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='ideas'
    )

    created_at = models.DateTimeField(auto_now_add=True)

    # @property
    # def score(self):
    #     result = self.votes.aggregate(total=Sum('value'))
    #     return result['total'] or 0

    def __str__(self):
        return self.title
