import uuid

import tagulous.models
from ckeditor.fields import RichTextField
from django.db import models

# Create your models here.
from django.urls import reverse
from django.utils.text import slugify

from tag.models import Tag


class Post(models.Model):
    POST_TYPE = (
        (1, 'Article'),
        (2, 'Job'),
        (3, 'Course'),
        (4, 'Project'),
    )

    identifier = models.UUIDField(default=uuid.uuid4, editable=False, unique=True)
    slug = models.SlugField(unique=True, null=True, blank=True)
    type = models.PositiveSmallIntegerField(choices=POST_TYPE, default=1)
    tags = tagulous.models.TagField(related_name='posts', to=Tag)

    author = models.ForeignKey('users.CustomUser', on_delete=models.CASCADE, related_name='blogs')
    title = models.CharField(max_length=255)
    body = RichTextField()
    preview = models.CharField(max_length=300, help_text='A short preview of this post that is shown in list of posts.')

    likes = models.ManyToManyField('users.CustomUser', blank=True)
    allow_comments = models.BooleanField(default=True)

    def save(self, *args, **kwargs):
        self.slug = slugify(f'{self.title} {self.identifier}', allow_unicode=True)
        super(Post, self).save(*args, **kwargs)

    def __str__(self):
        return f'{self.title}, by {self.author.first_name} {self.author.last_name}'

    @property
    def likes_count(self):
        return self.likes.count()

    @property
    def relative_url(self):
        return reverse('blog-post',
                       kwargs={
                           'slug': self.slug
                       })
