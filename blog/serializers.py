from rest_framework import serializers

from blog.models import Post


class PostSerializer(serializers.ModelSerializer):
    author = serializers.SlugRelatedField(slug_field='identifier',
                                          read_only=True)
    tags = serializers.SlugRelatedField(slug_field='name',
                                        read_only=True,
                                        many=True)

    class Meta:
        model = Post
        fields = ('identifier', 'type', 'tags', 'author', 'title', 'body', 'likes_count')
