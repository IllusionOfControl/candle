from django import forms


class BookForm(forms.Form):
    title = forms.CharField(label='Book title')
    description = forms.CharField(label='Description', required=False)
    author = forms.CharField(label='authors_id', required=False)
    publisher = forms.CharField(label='publisher_id', required=False)
    series = forms.CharField(label='series_id', required=False)
    tags = forms.CharField(label='tags_id', required=False)
    rating = forms.IntegerField(label='Rating', initial=0)

