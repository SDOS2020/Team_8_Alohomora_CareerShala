from ckeditor.fields import RichTextField
from django.db import models


# Create your models here.

class Post(models.Model):
    author = models.ForeignKey('users.CustomUser', on_delete=models.CASCADE, related_name='blogs')
    title = models.CharField(max_length=255)
    body = RichTextField()
    likes = models.ManyToManyField('users.CustomUser', blank=True)

    def __str__(self):
        return f'{self.title}, by {self.author.first_name} {self.author.last_name}'
