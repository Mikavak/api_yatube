from django.shortcuts import render
from rest_framework import viewsets
from .serializers import PostSerializer, GroupSerializer
  # Импортировали класс Response
from rest_framework import generics

from posts.models import Post, Group


class PostList(viewsets.ModelViewSet):
    queryset = Post.objects.all()
    serializer_class = PostSerializer


class GroupList(viewsets.ReadOnlyModelViewSet):
    queryset = Group.objects.all()
    serializer_class = GroupSerializer

# Create your views here.
