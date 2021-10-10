from django.http import Http404
from rest_framework import generics, permissions
from rest_framework import status, permissions
from rest_framework.views import APIView
from rest_framework.response import Response
from .models import Comment
from .serializers import CommentSerializer, CommentDetailSerializer
from drf_api.permissions import IsOwnerOrReadOnly


class CommentList(generics.ListCreateAPIView):
    """
    List comments or create a comment if logged in.
    Extending the ListAPIView means we  won’t have to write the get method  
    and the CreateAPIView takes  care of the post method.
    with generics, the request  is a part of the context object by default.  
    """
    serializer_class = CommentSerializer
    # the blw permission is to stop annyms users from commntin
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]
    queryset = Comment.objects.all()

    def perform_create(self, serializer):
        """
        to make sure  comments are associated with a user upon creation.  
        We do this with generics by  defining the perform_create method,  
        """
        serializer.save(owner=self.request.user)


class CommentDetail(generics.RetrieveUpdateDestroyAPIView):
    """
    Retrieve a comment, or update or delete it by id if you own it.
    to update and delete a comment, extend  the RetrieveUpdateDestroyAPI generic view.
    In order not to have to send  the post id every time I want to edit a comment,  
    set serializer_class  to CommentDetailSerializer.  
    """
    permission_classes = [IsOwnerOrReadOnly]
    serializer_class = CommentDetailSerializer
    queryset = Comment.objects.all()