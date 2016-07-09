from django.shortcuts import render, HttpResponse
from .models import BorrowBookLog, AddBookLog
from users.models import Library, LibUser
from books.models import Book


def libraries(request):
    libs = {l.username: 0 for l in Library.objects.all()}
    log = BorrowBookLog.objects.all()
    for field in log:
        libs[field.library.username] += 1
    sorted_libs = sorted(libs, key=libs.get, reverse=True)
    return HttpResponse(str(sorted_libs))


def users(request):
    library = None
    if request.user.is_authenticated:
        library = Library.objects.filter(username=request.user.username)
    if library:
        library = library[0]
        log = BorrowBookLog.objects.filter(library=library)
        users = {
            field.user.username:
            0 for field in AddUserLog.objects.filter(library=library)}
    else:
        log = BorrowBookLog.objects.all()
        users = {user.username: 0 for user in LibUser.objects.all()}
    for field in log:
        users[field.user.username] += 1
    sorted_users = sorted(users, key=users.get, reverse=True)
    return HttpResponse(str(sorted_users))


def books(request):
    library = None
    if request.user.is_authenticated:
        library = Library.objects.filter(username=request.user.username)
    if library:
        library = library[0]
        log = BorrowBookLog.objects.filter(library=library)
        books = {
            field.book.book.title:
            0 for field in AddBookLog.objects.filter(library=library)}
    else:
        log = BorrowBookLog.objects.all()
        books = {book.title: 0 for book in Book.objects.all()}
    for field in log:
        books[field.book.book.title] += 1
    sorted_books = sorted(books, key=books.get, reverse=True)
    return HttpResponse(str(sorted_books))


def books_not_return(request):
    if request.method == 'GET':
        try:
            lib = Library.objects.get(username=request.GET['library'])
            log_fields = BorrowBookLog(library=lib)
            books = {
                field.book.unique_id:
                field.user.username for field in log_fields if field}
            return HttpResponse("<br>".join(books))
        except:
            return HttpResponse("Incorrect data")
