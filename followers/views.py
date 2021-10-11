from rest_framework import generics, permissions
from .models import Follower
from .serializers import FollowerSerializer
from drf_api.permissions import IsOwnerOrReadOnly


class FollowerList(generics.ListCreateAPIView):
    """
    """
    serializer_class = FollowerSerializer
    # the blw permission is to stop annyms users from commntin
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]
    queryset = Follower.objects.all()

    def perform_create(self, serializer):
        """
        to make sure  followers are associated with a user upon creation.  
        We do this with generics by  defining the perform_create method,  
        """
        serializer.save(owner=self.request.user)

class FollowerDetail(generics.RetrieveDestroyAPIView):
    """
    Retrieve a follower,  or delete it by id if you own it.
    we didn’t extend the  UpdateAPIView, as we don’t need to update likes. 
    """
    permission_classes = [IsOwnerOrReadOnly]
    serializer_class = FollowerSerializer
    queryset = Follower.objects.all()