from rest_framework import generics, permissions

from votes.models import Vote
from votes.serializers import VoteSerializer


class VoteView(generics.CreateAPIView):

    queryset = Vote.objects.all()
    serializer_class = VoteSerializer
    permission_classes = [permissions.IsAuthenticated]
