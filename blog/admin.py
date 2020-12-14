from django.contrib import admin

# Register your models here.
from blog.forms import PostCreationForm
from blog.models import Post


class PostAdmin(admin.ModelAdmin):
    form = PostCreationForm

    # https://code.djangoproject.com/wiki/CookBookNewformsAdminAndUser
    # https://stackoverflow.com/a/855837/5394180
    def save_model(self, request, obj, form, change):
        obj.author = request.user
        obj.save()


admin.site.register(Post, PostAdmin)
