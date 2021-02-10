from django import forms
from .models import Book


class BookForm(forms.ModelForm):

    # TODO: Add a custom file field to restrict identical MIMETYPE
    files = forms.FileField(label='Book file', widget=forms.ClearableFileInput(attrs={'multiple': True}))

    class Meta:
        model = Book
        fields = ['title', 'description', 'rating', 'tags', 'series']