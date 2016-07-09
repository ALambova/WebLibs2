from django.db import models
import books
import users
from datetime import datetime


class BorrowBookLog(models.Model):
    library = models.ForeignKey('users.Library')
    user = models.ForeignKey('users.LibUser')
    book = models.ForeignKey('books.BookEntity')
    date_from = models.DateField(auto_now=True)
    date_to = models.DateField(null=True)


class AddBookLog(models.Model):
    library = models.ForeignKey('users.Library')
    book = models.ForeignKey('books.BookEntity')
    date = models.DateField(auto_now=True)
