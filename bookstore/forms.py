from django import forms
from .models import *


class BookForm(forms.ModelForm):

    cover = forms.FileField(label='Cover',
                            required=False)

    # TODO: Add a custom file field to restrict identical MIMETYPE
    files = forms.FileField(label='Book file',
                            widget=forms.ClearableFileInput(attrs={'multiple': True}),
                            required=False)

    class Meta:
        model = Book
        fields = ['title', 'description', 'rating', 'tags', 'series']


# class AuthorEditForm(forms.ModelForm):
#     class Meta:
#         model = Author
#
#
# class TagEditForm(forms.ModelForm):
#     class Meta:
#         model = Tag
#
#
# class SeriesEditForm(forms.ModelForm):
#     class Meta:
#         model = Series
#
#
# class PublisherEditForm(forms.ModelForm):
#     class Meta:
#         model = Publisher


class FileUploadForm(forms.Form):
    files = forms.FileField(label='Book file', widget=forms.ClearableFileInput(attrs={'multiple': True}))
