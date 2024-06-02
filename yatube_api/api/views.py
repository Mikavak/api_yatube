from django.shortcuts import get_object_or_404, render
from rest_framework import viewsets
from .serializers import PostSerializer, GroupSerializer
  # Импортировали класс Response
from rest_framework import generics
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework import status

from posts.models import Post, Group


class PostList(viewsets.ModelViewSet):
    queryset = Post.objects.all()
    serializer_class = PostSerializer

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)

    def perform_destroy(self, serializer):
        if serializer.author != self.request.user:
            return Response(status=status.HTTP_403_FORBIDDEN)
        else:
            serializer.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)

    # def perform_destroy(self, request, pk):
    #     post = get_object_or_404(Post, id=pk)
    #     if request.user != post.author:
    #         return Response(status=status.HTTP_403_FORBIDDEN)
        

class GroupList(viewsets.ReadOnlyModelViewSet):
    queryset = Group.objects.all()
    serializer_class = GroupSerializer

# Create your views here.
