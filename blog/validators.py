from django.core.exceptions import ValidationError

from blog.models import Post


def validate_post_type(post_type):
    if (not isinstance(post_type, int)) or (
            not any(post_type == allowed_post_type[0] for allowed_post_type in Post.POST_TYPE)):
        raise ValidationError
