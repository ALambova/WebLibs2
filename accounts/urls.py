from django.conf.urls import url
from . import views


urlpatterns = [
    url(r'^home/$', views.home),
    url(r'^register_library/$', views.LibraryRegistrationView.as_view()),
    url(r'^register_user/$', views.LibUserRegistrationView.as_view()),
    url(r'^login/$', views.LoginView.as_view()),
    url(r'^logout/$', views.LogOutView.as_view()),
    ]
    
