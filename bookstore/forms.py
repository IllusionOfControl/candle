from django import forms
from django.core.validators import FileExtensionValidator
from .models import *

VALID_FILES_EXT = ['pdf', 'djvu', 'epub', 'fb2', 'cbr', 'chm', 'html', 'mobi', 'odt', 'opf', 'rtf', 'txt']
VALID_COVER_EXT = ['jpg', 'jpeg', 'png']


class BookForm(forms.ModelForm):
    description = forms.CharField(required=False,
                                  widget=forms.Textarea)

    cover = forms.FileField(label='Cover',
                            required=False,
                            validators=[FileExtensionValidator(VALID_COVER_EXT)])

    files = forms.FileField(label='Book file',
                            widget=forms.ClearableFileInput(attrs={'multiple': True}),
                            required=False, validators=[FileExtensionValidator(VALID_FILES_EXT)])

    published_at = forms.DateField(label='published_at',
                                   widget=forms.DateInput(attrs={'type': 'date'}),
                                   required=False)

    class Meta:
        model = Book
        fields = ['title', 'description', 'authors', 'tags', 'series', 'publisher', 'published_at', 'isbn']


class FileUploadForm(forms.Form):
    files = forms.FileField(label='Book file',
                            widget=forms.ClearableFileInput(attrs={'multiple': True}),
                            validators=[FileExtensionValidator(VALID_FILES_EXT)])
