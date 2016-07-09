
from django.contrib import admin
from .models import Book, BookOtherInfo, BookEntity

admin.site.register(Book)
admin.site.register(BookOtherInfo)
admin.site.register(BookEntity)
# Register your models here.
