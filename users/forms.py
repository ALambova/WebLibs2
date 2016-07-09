from django import forms
from books import models
from .models import Library, LibUser


class AddBookForm(forms.ModelForm):
    other_info = forms.CharField(widget=forms.Textarea)

    class Meta:
        model = models.Book
        fields = [
            'ISBN', 'title', 'author',
            'description', 'publisher']


class AddUserForm(forms.Form):
    username = forms.CharField()
    date_from = forms.DateField()
    date_to = forms.DateField()


class BorrowBookForm(forms.Form):
    book = forms.CharField()
    user = forms.CharField()
    date_from = forms.CharField()
    date_to = forms.CharField()


class ReturnBookForm(forms.Form):
    book = forms.CharField()


class AddBookEntityForm(forms.Form):
    ISBN = forms.CharField()
