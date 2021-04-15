from django import forms
from django.core.validators import FileExtensionValidator
from .models import *


VALID_FILES_EXT = ['pdf', 'djvu', 'epub', 'fb2']
VALID_COVER_EXT = ['jpg', 'jpeg']


class BookForm(forms.ModelForm):
    description = forms.CharField(required=False,
                                  widget=forms.Textarea)

    cover = forms.FileField(label='Cover',
                            required=False,
                            validators=[FileExtensionValidator(VALID_COVER_EXT)])

    files = forms.FileField(label='Book file',
                            widget=forms.ClearableFileInput(attrs={'multiple': True}),
                            required=False, validators=[FileExtensionValidator(VALID_FILES_EXT)])

    class Meta:
        model = Book
        fields = ['title', 'description', 'rating', 'tags', 'series']


class FileUploadForm(forms.Form):
    files = forms.FileField(label='Book file',
                            widget=forms.ClearableFileInput(attrs={'multiple': True}),
                            validators=[FileExtensionValidator(VALID_COVER_EXT)])
