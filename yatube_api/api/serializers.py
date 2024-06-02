from rest_framework import serializers
from posts.models import Post, Group


class PostSerializer(serializers.ModelSerializer):
    author = serializers.StringRelatedField(read_only=True)

    class Meta:
        model = Post
        fields = ('id', 'text', 'pub_date', 'author')


class GroupSerializer(serializers.ModelSerializer):
    class Meta:
        model = Post
        fields = ('id', 'title', 'slug', 'desription')
