from django.shortcuts import render, HttpResponse
from .models import Book

def books_list(request):
    books = [str(book) for book in Book.objects.all()]
    return HttpResponse("<br>".join(books))

def authors_list(request):
    authors = [book.author for book in Book.objects.all()]
    return HttpResponse("<br>".join(authors))

def book_details(request, *args, **kwargs):
    if request.method == 'GET':
        book = Book.objects.filter(ISBN=request.GET['ISBN'])
        if book:
            data = book.title + "<br>"
            + book.author + "<br>" + book.description
            + "<br>" + book.rating
            return HttpResponse(data)
        else:
            return HttpResponse("This book is not registered")


def books_by_author(request, *args, **kwargs):
    if request.method == 'GET':
        books = [
            str(book) for book in Book.objects.filter(
                author=request.GET['author'])]
    return HttpResponse("<br>".join(books))
