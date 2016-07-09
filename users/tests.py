from django.test import TestCase, Client
from django.contrib.auth import authenticate
from django.core.urlresolvers import reverse
import datetime
from users.models import Library, LibUser, Subscription
from users.exceptions import SubscriptionExpiredError
from books.models import Book, BookEntity, BookOtherInfo
from . import views



class TestLibraryCase(TestCase):
    def setUp(self):
        Library.objects.create(
            username="TestLib", password="test123",
            email="testlib@abv.bg", address="Sofiq, Lozenec",
            phoneNum="0765231463", director="Ivan Ivanov")
        Library.objects.create(
            username="TestLib2", password="123test",
            email="testlib2@abv.bg", address="Burgas, Lazur",
            phoneNum="0888635278", director="Katerina Berova")
        LibUser.objects.create(
            username="TestUser", password="user123",
            email="user@abv.bg", address="Burgas, Lazur 74",
            phoneNum="0876325412", first_name="Mariq",
            last_name="Petrova")
        LibUser.objects.create(
            username="TestUser2", password="123user",
            email="user2@abv.bg", address="Burgas, Lazur 74",
            phoneNum="0898325412", first_name="Ani",
            last_name="Petrova")
        Book.objects.create(
            ISBN=654321, title='Harry Potter',
            author='JKR', publisher='Unknown',
            description='Interesting...', rating=0)
        client = Client()

    def test_add_and_remove_user(self):
        library = Library.objects.get(username="TestLib")
        library2 = Library.objects.get(username="TestLib2")
        user = LibUser.objects.get(username="TestUser")
        user2 = LibUser.objects.get(username="TestUser2")
        library.add_user(
            user,
            datetime.date(day=5, month=7, year=2016),
            datetime.date(day=5, month=8, year=2016))
        library.add_user(
            user2,
            datetime.date(day=1, month=5, year=2016),
            datetime.date(day=1, month=6, year=2016))
        library2.add_user(
            user,
            datetime.date(day=1, month=5, year=2016),
            datetime.date(day=1, month=6, year=2016))
        users = [s.user for s in Subscription.objects.filter(library=library)]
        self.assertEqual(set(users), {user, user2})
        users = [s.user for s in Subscription.objects.filter(library=library2)]
        self.assertEqual(set(users), {user})

    def test_add_book(self):
        lib = Library.objects.get(username='TestLib')
        lib.add_book(
            {
                'ISBN': '123456', 'title': 'Harry Potter',
                'author': 'JKR', 'publisher': 'Unknown',
                'description': 'Interesting...', 'rating': 0,
            }
        )
        book = Book.objects.get(ISBN='123456')
        self.assertEqual(book.title, 'Harry Potter')
        self.assertEqual(book.author, 'JKR')
        self.assertEqual(book.publisher, 'Unknown')
        self.assertEqual(book.description, 'Interesting...')
        lib2 = Library.objects.get(username='TestLib2')
        lib2.add_book_info(book, 'description', 'other info')
        book_info = BookOtherInfo.objects.get(library=lib2, book=book)
        self.assertEqual(book_info.description, 'description')
        self.assertEqual(book_info.other_info, 'other info')

    def test_add_entity(self):
        lib = Library.objects.get(username='TestLib')
        book = Book.objects.get(ISBN='654321')
        unique_id = lib.add_entity(book)
        be = BookEntity.objects.get(unique_id=unique_id)
        self.assertEqual(be.library, lib)
        self.assertEqual(be.book, book)

    def test_borrow_book(self):
        lib = Library.objects.get(username='TestLib')
        user = LibUser.objects.get(username='TestUser')
        user2 = LibUser.objects.get(username='TestUser2')
        book = Book.objects.get(ISBN='654321')
        unique_id = lib.add_entity(book)
        be = BookEntity.objects.get(unique_id=unique_id)
        date_from = datetime.date(day=1, month=7, year=2016)
        date_to = datetime.date(day=1, month=8, year=2016)
        lib.add_user(user, date_from, date_to)
        date_from2 = datetime.date(day=1, month=6, year=2016)
        date_to2 = datetime.date(day=1, month=7, year=2016)
        lib.add_user(user2, date_from2, date_to2)
        self.assertEqual(be.borrowed, False)
        lib.borrow_book(be, user, date_from, date_to)
        self.assertEqual(be.borrowed, True)
        lib.return_book(be, user)
        self.assertEqual(be.borrowed, False)
        self.assertRaises(
            SubscriptionExpiredError,
            lib.borrow_book, be, user2, date_from, date_to)

    def test_views(self):
        pass
