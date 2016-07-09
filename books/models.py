from django.db import models
import uuid


class Book(models.Model):
    title = models.CharField(max_length=30)
    author = models.CharField(max_length=50)
    rating = models.FloatField(default=0)
    description = models.TextField(blank=True, default="")
    ISBN = models.CharField(max_length=20)
    publisher = models.CharField(max_length=50)

    def __str__(self):
        return self.ISBN + " , "
        + self.title + " , "
        + self.author

    def add_other_info(self, library, lib_descr, other_info=""):
        book_info = BookOtherInfo.objects.filter(library=library, book=self)
        if book_info:
            if lib_descr:
                book_info[0].description = lib_descr
            if other_info:
                book_info[0].other_info = other_info
            book_info.save()
        else:
            BookOtherInfo.objects.create(
                book=self, library=library, description=lib_descr,
                other_info=other_info)


class BookOtherInfo(models.Model):
    library = models.ForeignKey('users.Library', null=True)
    book = models.ForeignKey(Book, null=True)
    description = models.TextField(blank=True)
    other_info = models.TextField(blank=True)


class BookEntity(models.Model):

    unique_id = models.UUIDField(
        default=uuid.uuid4, unique=True)
    book = models.ForeignKey(Book, null=True)
    library = models.ForeignKey('users.Library', null=True)
    borrowed = models.BooleanField(default=False)

    def borrow(self, user, date_from, date_to):
        if self.borrowed is True:
            return False
        self.borrowed = True
        self.save()
        return True

    def return_book(self):
        self.borrowed = False
        self.save()


class SuggestedBook(models.Model):
    book = models.ForeignKey('books.Book', null=True)
    vote = models.IntegerField(default=0)
