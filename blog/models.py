import uuid

import tagulous.models
from ckeditor.fields import RichTextField
from django.conf import settings
from django.contrib.sites.models import Site
from django.db import models

# Create your models here.
from django.urls import reverse
from django.utils.text import slugify
from django_bleach.models import BleachField

from tag.models import Tag


class Post(models.Model):
    POST_TYPE = (
        (1, 'Article'),
        (2, 'Course'),
        (3, 'Job'),
        (4, 'Project'),
    )

    identifier = models.UUIDField(default=uuid.uuid4, editable=False, unique=True)
    slug = models.SlugField(unique=True, null=True, blank=True, max_length=512)
    type = models.PositiveSmallIntegerField(choices=POST_TYPE, default=1)
    tags = tagulous.models.TagField(related_name='posts', to=Tag)

    author = models.ForeignKey('users.CustomUser', on_delete=models.CASCADE, related_name='blogs')
    title = models.CharField(max_length=255)
    body = BleachField()
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

    def get_absolute_url(self):
        domain = Site.objects.get_current().domain
        protocol = "https" if settings.PRODUCTION_SERVER else "http"
        absolute_url = f'{protocol}://{domain}{self.relative_url}'
        return absolute_url


class Submission(models.Model):
    student_profile = models.ForeignKey('users.StudentProfile', on_delete=models.CASCADE,
                                        related_name='student_submissions')
    uploaded_file = models.FileField(upload_to='student_uploads/')
    uploaded_time = models.DateTimeField(auto_now_add=True)
    post = models.ForeignKey('blog.Post', on_delete=models.CASCADE, related_name='post_submissions')

    class Meta:
        unique_together = ('student_profile', 'post')
