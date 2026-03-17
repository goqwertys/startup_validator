from datetime import timedelta

from django.db.models import Sum, ExpressionWrapper, F, FloatField, Value
from django.db.models.functions import Coalesce, Now, Extract
from django.utils import timezone
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.decorators import action
from rest_framework.filters import OrderingFilter
from rest_framework.permissions import IsAuthenticatedOrReadOnly
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet

from ideas.filters import IdeaFilter
from ideas.models import Idea
from ideas.permissions import IsOwnerOrReadOnly
from ideas.serializers import IdeaSerializer


class IdeaViewSet(ModelViewSet):
    queryset = Idea.objects.all()
    serializer_class = IdeaSerializer
    permission_classes = [IsAuthenticatedOrReadOnly, IsOwnerOrReadOnly]

    filter_backends = [DjangoFilterBackend, OrderingFilter]
    filterset_class = IdeaFilter
    ordering_fields = ["created_at", "score", "trending"]

    def perform_create(self, serializer):
        serializer.save(creator=self.request.user)

    # ----------------------------------------
    # Annotation method
    # ----------------------------------------
    def annotate_queryset(self, qs):
        return (
            qs.annotate(score=Coalesce(Sum('votes__value'), 0))
            .annotate(
                age_seconds=Extract(
                    Now() - F('created_at'),
                    'epoch'
                )
            )
            .annotate(
                age_days=ExpressionWrapper(
                    F('age_seconds') / Value(86400.0),
                    output_field=FloatField()
                )
            )
            .annotate(
                trending=ExpressionWrapper(
                    F('score') / (F('age_days') + Value(2.0)),
                    output_field=FloatField()
                )
            )
        )
    # ----------------------------------------
    # Base queryset
    # ----------------------------------------
    def get_queryset(self):
        return self.annotate_queryset(Idea.objects.all()).order_by('-created_at')

    # ----------------------------------------
    # Top 10 ideas
    # ----------------------------------------
    @action(detail=False, methods=['get'], url_path='top')
    def top(self, request):
        period = request.query_params.get('period')  # week / day
        queryset = self.annotate_queryset(Idea.objects.all())

        if period == 'week':
            week_ago = timezone.now() - timedelta(days=7)
            queryset = queryset.filter(created_at__gte=week_ago)

        top_ideas = queryset.order_by('-score')[:10]
        serializer = self.get_serializer(top_ideas, many=True)
        return Response(serializer.data)

    # ----------------------------------------
    # Trending ideas
    # ----------------------------------------
    @action(detail=False, methods=['get'], url_path='trending')
    def trending(self, request):
        queryset = self.annotate_queryset(Idea.objects.all()).order_by('-trending')
        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)
