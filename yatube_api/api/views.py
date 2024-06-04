from posts.models import Comment, Group, Post, User
from rest_framework import status, viewsets
from rest_framework.decorators import api_view
from rest_framework.response import Response

from .serializers import (CommentSerializer, GroupSerializer, PostSerializer,
                          UserSerializer)


class PermissionDenied(Exception):
    pass


class PostList(viewsets.ModelViewSet):
    queryset = Post.objects.all()
    serializer_class = PostSerializer

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)

    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        if instance.author != request.user:
            return Response(status=status.HTTP_403_FORBIDDEN)
        self.perform_destroy(instance)
        return Response(status=status.HTTP_204_NO_CONTENT)

    def update(self, request, *args, **kwargs):
        partial = kwargs.pop('partial', False)
        instance = self.get_object()
        if instance.author != request.user:
            return Response(status=status.HTTP_403_FORBIDDEN)
        serializer = self.get_serializer(
            instance, data=request.data, partial=partial)
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)

        if getattr(instance, '_prefetched_objects_cache', None):
            instance._prefetched_objects_cache = {}

        return Response(serializer.data)


class GroupList(viewsets.ReadOnlyModelViewSet):
    queryset = Group.objects.all()
    serializer_class = GroupSerializer


class UserViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer


@api_view(['GET', 'POST'])
def comments(request, post_id):
    # post_id = request.kwargs.get('post_id')
    post = Post.objects.get(id=post_id)
    comments = Comment.objects.filter(post=post_id)
    if request.user.is_authenticated:
        if post.author != request.user:
            return Response(status=status.HTTP_403_FORBIDDEN)
    if request.method == 'POST':
        serializer = CommentSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(author=request.user, post_id=post_id)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    else:
        serializer = CommentSerializer(comments, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


@api_view(['GET', 'PUT', 'PATCH', 'DELETE'])
def one_comment(request, post_id, comment_id):
    comment = Comment.objects.get(pk=comment_id)
    serializer = CommentSerializer(comment)

    if request.method == 'GET':
        return Response(serializer.data, status=status.HTTP_200_OK)
    
    if request.user.is_authenticated:
        if request.method == 'DELETE':
            if comment.author != request.user:
                return Response(status=status.HTTP_403_FORBIDDEN)
            comment.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)
        if request.method == 'PUT' or request.method == 'PATCH':
            if comment.author != request.user:
                return Response(status=status.HTTP_403_FORBIDDEN)
            serializer = CommentSerializer(
                comment, data=request.data, partial=True)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    else:
        return Response(status=status.HTTP_401_UNAUTHORIZED)
