from rest_framework import serializers

from blog.models import Post


class PostSerializer(serializers.ModelSerializer):
    author = serializers.SlugRelatedField(slug_field='full_name',
                                          read_only=True)
    tags = serializers.SlugRelatedField(slug_field='name',
                                        read_only=True,
                                        many=True)

    class Meta:
        model = Post
        fields = ('identifier', 'type', 'tags', 'author', 'title', 'body', 'likes_count', 'absolute_url')


class PostMiniSerializer(PostSerializer):
    class Meta:
        model = Post
        fields = ('type', 'tags', 'author', 'title', 'preview', 'likes_count', 'absolute_url')
