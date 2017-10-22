from django.shortcuts import render
from .api import *

# Create your views herel
from django.conf.urls import url, include

urlpatterns = [
    url(r'^create', CreateUserView.as_view()),
    url(r'^me', GetUserView.as_view()),
]
