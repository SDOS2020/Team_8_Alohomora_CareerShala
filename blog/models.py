import uuid

import tagulous.models
from ckeditor.fields import RichTextField
from django.db import models

# Create your models here.
from django.urls import reverse
from django.utils.text import slugify


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
    tags = tagulous.models.TagField()

    author = models.ForeignKey('users.CustomUser', on_delete=models.CASCADE, related_name='blogs')
    title = models.CharField(max_length=255)
    body = RichTextField()

    likes = models.ManyToManyField('users.CustomUser', blank=True)

    def save(self, *args, **kwargs):
        self.slug = slugify(f'{self.title} {self.identifier}', allow_unicode=True)
        super(Post, self).save(*args, **kwargs)

    def __str__(self):
        return f'{self.title}, by {self.author.first_name} {self.author.last_name}'
