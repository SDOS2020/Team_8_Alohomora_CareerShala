from ckeditor.widgets import CKEditorWidget
from django import forms
from django.core.exceptions import ValidationError
from django_bleach.forms import BleachField

from blog.models import Post, Submission


class PostCreationForm(forms.ModelForm):
    body = BleachField()

    class Meta:
        model = Post
        fields = ('title', 'body', 'preview', 'type', 'tags', 'allow_comments')


class SubmissionForm(forms.ModelForm):
    post_identifier = forms.UUIDField()

    class Meta:
        model = Submission
        fields = ('uploaded_file',)

    def clean_post(self):
        post_identifier = self.cleaned_data['post']
        if Post.objects.filter(identifier=post_identifier).exists():
            if Post.objects.get(identifier=post_identifier).type == 4:
                return post_identifier
            raise ValidationError('You cannot submit anything on this post')
        raise ValidationError('No such post exists')
