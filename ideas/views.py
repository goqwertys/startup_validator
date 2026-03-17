from rest_framework.permissions import IsAuthenticatedOrReadOnly
from rest_framework.viewsets import ModelViewSet

from ideas.models import Idea
from ideas.serializers import IdeaSerializer


class IdeaViewSet(ModelViewSet):

    queryset = Idea.objects.all().order_by('-created_at')
    serializer_class = IdeaSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]

    def perform_create(self, serializer):
        serializer.save(creator=self.request.user)
