from django.core.exceptions import ValidationError

from blog.methods import is_int
from blog.models import Post


def validate_post_type(post_type):
    if not ((is_int(post_type)) and (
    any(int(post_type) == allowed_post_type[0] for allowed_post_type in Post.POST_TYPE))):
        raise ValidationError(message="post_type invalid")
