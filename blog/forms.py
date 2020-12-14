from ckeditor.widgets import CKEditorWidget
from django import forms
from django_bleach.forms import BleachField

from blog.models import Post


class PostCreationForm(forms.ModelForm):
    body = BleachField()

    class Meta:
        model = Post
        fields = ('title', 'body', 'preview', 'type', 'tags', 'allow_comments')
