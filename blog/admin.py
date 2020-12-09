from django.contrib import admin

# Register your models here.
from blog.forms import PostCreationForm
from blog.models import Post


class PostAdmin(admin.ModelAdmin):
    form = PostCreationForm


admin.site.register(Post, PostAdmin)
