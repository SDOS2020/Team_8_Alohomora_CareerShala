from ckeditor.widgets import CKEditorWidget
from django import forms

from blog.models import Post


class PostCreationForm(forms.ModelForm):
    body = forms.CharField(widget=CKEditorWidget())

    class Meta:
        model = Post
        fields = ('title', 'body', 'preview', 'type', 'tags', 'allow_comments')
