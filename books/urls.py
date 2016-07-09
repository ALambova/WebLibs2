from django.conf.urls import url
from . import views


urlpatterns = [
    url(r'^list/$', views.books_list),
    url(r'^authors/$', views.authors_list),
    url(r'^book_details/$', views.book_details),
    url(r'^books_by_author/$', views.books_by_author),
    ]
