from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import OrderingFilter
from rest_framework.permissions import IsAuthenticatedOrReadOnly
from rest_framework.viewsets import ModelViewSet

from ideas.filters import IdeaFilter
from ideas.models import Idea
from ideas.permissions import IsOwnerOrReadOnly
from ideas.serializers import IdeaSerializer


class IdeaViewSet(ModelViewSet):

    queryset = Idea.objects.all().order_by('-created_at')
    serializer_class = IdeaSerializer
    permission_classes = [IsAuthenticatedOrReadOnly, IsOwnerOrReadOnly]

    filter_backends = [DjangoFilterBackend, OrderingFilter]
    filterset_class = IdeaFilter
    ordering_fields = ['created_at']

    def perform_create(self, serializer):
        serializer.save(creator=self.request.user)
