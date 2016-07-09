from django.conf.urls import url
from . import views


urlpatterns = [
    url(r'^libraries/$', views.libraries),
    url(r'^users/$', views.users),
    url(r'^books/$', views.books),
    ]
