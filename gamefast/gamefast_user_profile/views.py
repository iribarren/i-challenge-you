from django.shortcuts import render
from .api import *

# Create your views herel
from django.conf.urls import url, include

urlpatterns = [
    url(r'^/users/create', CreateUserView.as_view, name='create-user'),
]
