from django.conf.urls import url
from . import views


urlpatterns = [
    url(r'^add_book/$', views.add_book),
    url(r'^add_user/$', views.add_user),
    url(r'^add_book_entity/$', views.add_book_entity),
    url(r'^borrow_book/$', views.borrow_book),
    url(r'^return_book/$', views.return_book),
    url(r'^library_details/', views.library_details),
    url(r'^user_details/', views.user_details),
    url(r'^user_libraries/', views.user_libraries),
    url(r'^library_users/', views.library_users),
    url(r'^library_books/', views.library_books),
    ]
