from django import views
from django.contrib import admin
from django.urls import path
from blogparsing_sub_main import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.index),


]
