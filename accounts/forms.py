from django import forms
from books import models
from users.models import Library, LibUser
from registration.forms import RegistrationForm


class LibraryRegistrationForm(RegistrationForm):
    address = forms.CharField()
    phoneNum = forms.CharField()
    director = forms.CharField()
    otherInf = forms.CharField(widget=forms.Textarea)

    class Meta:
        model = Library
        fields = ['email', 'username', 'phoneNum', 'address', 'director']

class LibUserRegistrationForm(RegistrationForm):
    address = forms.CharField()
    phoneNum = forms.CharField()

    class Meta:
        model = LibUser
        fields = ['email', 'username', 'phoneNum', 'address']


class AddBookForm(forms.ModelForm):
    other_info = forms.CharField(widget=forms.Textarea)

    class Meta:
        model = models.Book
        fields = [
            'ISBN', 'title', 'author',
            'description', 'publisher']
        required_fields = [
            'ISBN', 'title', 'author',
            'description', 'publisher']
