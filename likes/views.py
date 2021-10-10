from rest_framework import generics, permissions
from rest_framework import status, permissions
from rest_framework.views import APIView
from rest_framework.response import Response
from .models import Like
from .serializers import LikeSerializer
from drf_api.permissions import IsOwnerOrReadOnly


class LikeList(generics.ListCreateAPIView):
    """
    List like or create a like if logged in.
    Extending the ListAPIView means we  won’t have to write the get method  
    and the CreateAPIView takes  care of the post method.
    with generics, the request  is a part of the context object by default.  
    """
    serializer_class = LikeSerializer
    # the blw permission is to stop annyms users from commntin
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]
    queryset = Like.objects.all()

    def perform_create(self, serializer):
        """
        to make sure  comments are associated with a user upon creation.  
        We do this with generics by  defining the perform_create method,  
        """
        serializer.save(owner=self.request.user)


class LikeDetail(generics.RetrieveDestroyAPIView):
    """
    Retrieve a like,  or delete it by id if you own it.
    we didn’t extend the  UpdateAPIView, as we don’t need to update likes. 
    """
    permission_classes = [IsOwnerOrReadOnly]
    serializer_class = LikeSerializer
    queryset = Like.objects.all()