from django.shortcuts import render

# Create your views here.
from errors.forms import ErrorForm


def error(request, error_dict=None):  # TODO can we make it a POST redirect?
    if error_dict is None:
        error_dict = {}
    error_form = ErrorForm(error_dict)
    error_object = {}
    if error_form.is_valid():
        error_object['title'] = error_form.cleaned_data['title']
        error_object['body'] = error_form.cleaned_data['body']
    else:
        error_object['title'] = "Bad Request"
        error_object['body'] = ""
    return render(request, 'errors/error.html', context={'error': error_object})
