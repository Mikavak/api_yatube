from django.shortcuts import render
from rest_framework import generics

from .serializers import PostSerializer

from posts.models import Post


class PostList(generics.ListCreateAPIView):
    queryset = Post.objects.all()
    serializer_class = PostSerializer

# Create your views here.
