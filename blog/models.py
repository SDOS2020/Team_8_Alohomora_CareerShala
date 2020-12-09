from django.db import models
from ckeditor.fields import RichTextField


# Create your models here.
class Post(models.Model):
    author = models.ForeignKey('users.CustomUser', on_delete=models.CASCADE, related_name='posts')
    title = models.CharField(max_length=255)
    body = RichTextField()
    likes = models.ManyToManyField('users.CustomUser', related_name='liked_posts', blank=True)

    def total_likes(self):
        return self.likes.count()

    def __str__(self):
        return f'{self.title}, by {self.author.first_name} {self.author.last_name}'
