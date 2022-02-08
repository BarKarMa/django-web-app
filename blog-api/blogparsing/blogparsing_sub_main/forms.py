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
            'word_count',
            'top_words',
        )
        widgets = {
            'title': forms.TextInput,
            'date': forms.DateTimeField,
            'author': forms.TextInput,
            'text': forms.TextInput,
            'word_count': forms.IntegerField,
            'top_words': forms.TextInput,

        }


class YearChoosen(forms.ModelForm):
    years = forms.Select(choices=[])
