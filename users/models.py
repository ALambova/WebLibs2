from django.db import models
from django.contrib.auth.models import AbstractUser
from books.models import Book, BookEntity, SuggestedBook
from log.models import BorrowBookLog, AddBookLog
import datetime
from . import exceptions
from django.core.mail import send_mail



class CustomUser(AbstractUser):
    address = models.CharField(max_length=50)
    phoneNum = models.CharField(max_length=15)
    is_library = models.BooleanField(default=False)


class LibUser(CustomUser):
    EGN = models.CharField(max_length=10, default="")

    class Meta:
        verbose_name = 'LibUser'

    def suggest_book(self, book):
        if not SuggestedBook.objects.filter(book=book):
            SuggestedBook.objects.create(book=book)

    def vote_for_book(self, book):
        sb = SuggestedBook.objects.filter(book=book)
        if sb:
            sb[0].vote = sb[0].vote + 1


class Library(CustomUser):
    director = models.CharField(max_length=50)
    otherInf = models.TextField(max_length=500, blank=True)

    class Meta:
        verbose_name_plural = 'Libraries'

    def add_user(self, user, date_from, date_to):
        subscription = Subscription.objects.filter(user=user, library=self)
        if not subscription:
            Subscription.objects.create(
                user=user, library=self,
                date_from=date_from, date_to=date_to)
        else:
            subscription[0].renew(date_from, date_to)
            # AddUserLog.objects.create(library=self, user=user)

    def add_book(self, book_dict):
        book = Book.objects.filter(ISBN=book_dict['ISBN'])
        if book:
            book = book[0]
        else:
            book = Book.objects.create(
                ISBN=book_dict['ISBN'], title=book_dict['title'],
                author=book_dict['author'],
                description=book_dict['description'],
                publisher=book_dict['publisher'], rating=book_dict['rating'])
        return book

    def add_book_info(self, book, lib_descr="", lib_info=""):
        if lib_descr or lib_info:
            book.add_other_info(self, lib_descr, lib_info)

    def add_entity(self, book):
        be = BookEntity.objects.create(
            book=book, library=self)
        AddBookLog.objects.create(library=self, book=be)
        return str(be.unique_id)

    def remove_entity(self, number):
        be = BookEntity.objects.filter(unique_id=number)
        if be:
            be[0].delete()

    def borrow_book(self, book, user, date_from, date_to):
        subscr = Subscription.objects.filter(library=self, user=user)
        if not subscr:
            raise exceptions.NoSubscriptionError
        if not subscr[0]:
            raise exceptions.SubscriptionExpiredError
        if BookEntity.objects.filter(
                unique_id=book.unique_id, library=self):
            BorrowBookLog.objects.create(
                library=self, book=book, user=user,
                date_from=date_from, date_to=date_to)
            return book.borrow(user, date_from, date_to)
        return False

    def return_book(self, book, user):
        # be = BookEntity.objects.filter(unique_id=book, library=self)
        if BookEntity.objects.filter(
                unique_id=book.unique_id, library=self):
            book.return_book()


class Subscription(models.Model):
    library = models.ForeignKey(Library, null=True)
    user = models.ForeignKey(LibUser, null=True)
    date_from = models.DateField(null=True)
    date_to = models.DateField(null=True)

    def __bool__(self):
        today = datetime.datetime.now()
        if self.date_to.year < today.year:
            return False
        if self.date_to.month < today.month:
            return False
        if self.date_to.month > today.month:
            return True
        if self.date_to.day < today.day:
            return False
        return True

    def renew(self, date_from, date_to):
        self.date_from = date_from
        self.date_to = date_to

    def send_emails(self, message):
        log_fields = BorrowBookLog(library=self)
        users = [field.user.email for field in log_fields if field]
        for user in users:
            send_mail(
                "Not returned book",
                message,
                self.email,
                users,
                fail_silently=True)

# Create your models here.
