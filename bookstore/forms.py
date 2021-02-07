from django import forms
from .models import Book


class BookForm(forms.ModelForm):

    file = forms.FileField(label='Book file')

    class Meta:
        model = Book
        fields = ['title', 'description', 'rating']
