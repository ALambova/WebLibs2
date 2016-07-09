from django.shortcuts import render, HttpResponse, redirect
from . import forms
from books.models import Book, BookEntity
from .models import Library, LibUser
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import Group
from django.views.generic import FormView, RedirectView
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib.auth.mixins import LoginRequiredMixin
import datetime
from . import exceptions
import books
from .models import Subscription

from books.goodreads import search_book


class Response404(HttpResponse):
    status_code = 404


class Response403(HttpResponse):
    status_code = 403


def is_library(view, *args, **kwargs):
    def _decorated(request):
        if request.user.is_library:
            return view(request)
        else:
            return Response403("Permission denied!")
    return _decorated


def is_user(view, *args, **kwargs):
    def _decorated(request):
        if not request.user.is_library:
            return view(request)
        else:
            return Response403("Permission denied!")
    return _decorated


@login_required(login_url="http://127.0.0.1:8000/accounts/login/")
@is_library
def user_details(request, *args, **kwarg1s):
    form = forms.nqkvaForm()
    if request.method == 'POST':
        name = request.POST['name']
        # get some data
        return render(request, 'nqkvo.html', {'form': form, 'entries': name})

    return render(request, 'nqkvo.html', {'form': form})


def library_details(request, *args, **kwargs):
    if request.method == 'GET':
        try:
            lib = Library.objects.get(username=request.GET['library'])
            data = lib.username + "<br>" + lib.address + "<br>" + lib.phoneNum + "<br>" + lib.otherInf
            return HttpResponse(data)
        except:
            return Response404("Incorrect data")

@login_required(login_url="http://127.0.0.1:8000/accounts/login/")
@is_library
def user_details(request, *args, **kwargs):
    if request.method == 'GET':
        try:
            user = LibUser.objects.get(username=request.GET['username'])
            data = user.first_name + "<br>" + user.last_name + "<br>" + user.address + "<br>" + user.phoneNum + "<br>" + user.EGN
            return HttpResponse(data)
        except:
            return Response404("Incorrect data")


@login_required(login_url="http://127.0.0.1:8000/accounts/login/")
@is_library
def add_user(request, *args, **kwargs):
    form = forms.AddUserForm()
    if request.method == 'POST':
        # request.user.add_user(request.POST)
        user = LibUser.objects.filter(username=request.POST['username'])
        if user:
            user = user[0]
        else:
            return Response404("User does not exist!")
        library = Library.objects.get(username=request.user.username)
        library.add_user(
            user, request.POST['date_from'], request.POST['date_to'])
        return render(request, 'template.html', {'form': form})
    return render(request, 'template.html', {'form': form}, status=404)


@login_required(login_url="http://127.0.0.1:8000/accounts/login/")
@is_library
def add_book(request, *args, **kwargs):
    form = forms.AddBookForm()
    user = Library.objects.get(username=request.user.username)
    if request.method == 'POST':
        book_dict = search_book(request.POST['ISBN'])
        if not book_dict:
            book_dict['ISBN'] = request.POST['ISBN']
            book_dict['title'] = request.POST['title']
            book_dict['author'] = request.POST['author']
            book_dict['publisher'] = request.POST['publisher']
            book_dict['description'] = request.POST['description']
            book_dict['rating'] = 0

        book = user.add_book(book_dict)
        if request.POST['description'] or request.POST['other_info']:
            user.add_book_info(
                book, request.POST['description'],
                request.POST['other_info'])

            # Library.objects.all()[0].add_book(request.POST)
        return render(request, 'template.html', {'form': form})
    return render(request, 'template.html', {'form': form}, status=400)


@login_required(login_url="http://127.0.0.1:8000/accounts/login/")
@is_library
def add_book_entity(request):
    form = forms.AddBookEntityForm()
    if request.method == 'POST':
        book = Book.objects.filter(ISBN=request.POST['ISBN'])
        if book:
            book = book[0]
        else:
            return redirect(
                'http://127.0.0.1:8000/users/add_book/', status=404)
        user = Library.objects.get(username=request.user.username)
        be = user.add_entity(book)
        return HttpResponse("ID: "+be)
    return render(request, 'template.html', {'form': form}, status=400)


@login_required(login_url="http://127.0.0.1:8000/accounts/login/")
@is_library
def borrow_book(request):
    form = forms.BorrowBookForm()
    if request.method == 'POST':
        try:
            book = BookEntity.objects.get(
                unique_id=request.POST['book'])
            library = Library.objects.get(
                username=request.user.username)
            user = LibUser.objects.get(
                username=request.POST['user'])
            library.borrow_book(
                book, user, request.POST['date_from'],
                request.POST['date_to'])
        except exceptions.NoSubscriptionError:
            render(
                request, 'template.html',
                {'form': form, 'entries': 'User has not subscription'})
        except exceptions.SubscriptionExpiredError:
            render(
                request, 'template.html',
                {'form': form, 'entries': 'User subscription is expired'})
        except books.exceptions.BorrowedBookError:
            render(
                request, 'template.html',
                {'form': form, 'entries': 'Book has been already borrowed'})
        except:
            render(
                request, 'template.html',
                {'form': form, 'entries': 'Incorrect data'}, status=404)
    return render(request, 'template.html', {'form': form})


@login_required(login_url="http://127.0.0.1:8000/accounts/login/")
@is_library
def return_book(request, *args, **kwargs):
    form = forms.ReturnBookForm()
    if request.method == 'POST':
        try:
            book = BookEntity.objects.get(
                unique_id=request.POST['book'])
            library = Library.objects.get(
                username=request.user.username)
            user = LibUser.objects.get(
                username=request.POST['user'])
            library.return_book(book, user)
        except:
            render(
                request, 'template.html',
                {'form': form, 'entries': 'Incorrect data'}, status=404)
    return render(request, 'template.html', {'form': form})


@login_required(login_url="http://127.0.0.1:8000/accounts/login/")
@is_user
def user_libraries(request):
    user = request.user
    subscr = Subscription.objects.filter(user=user)
    libraries = [s.library for s in subscr if s]
    return HttpResponse("<br>".join(libraries))


@login_required(login_url="http://127.0.0.1:8000/accounts/login/")
@is_library
def library_users(request):
    library = request.user
    subscr = Subscription.objects.filter(user=library)
    users = [s.user for s in subscr if s]
    return HttpResponse("<br>".join(users))


@login_required(login_url="http://127.0.0.1:8000/accounts/login/")
@is_library
def library_books(request):
    library = request.user
    entities = BookEntity.objects.filter(library=library)
    books = {str(be.book) for be in entities}
    return HttpResponse("<br>".join(books))
