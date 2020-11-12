from django import forms


class ErrorForm(forms.Form):
    title = forms.CharField(label="Title", max_length=100, required=True)
    body = forms.CharField(label="Body", max_length=1000, required=False)
