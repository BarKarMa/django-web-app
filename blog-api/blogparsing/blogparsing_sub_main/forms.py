# from tkinter import Widget
from django import forms

from .models import BlogNews

class NewsForm(forms.ModelForm):

    class Meta:
        model = BlogNews
        fields = (
            'title',
            'date',
            'author',
            'text',
            'word_count'
        )
        widgets = {
            'title': forms.TextInput,
            'date': forms.DateTimeField,
            'author': forms.TextInput,
            'text': forms.TextInput,
            'word_count': forms.IntegerField,

        }


class YearChoosen(forms.ModelForm):
    years = forms.Select(choices=['2020', '2021','2019','2018'])
