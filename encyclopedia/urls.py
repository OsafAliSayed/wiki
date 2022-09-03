from django.urls import path

from . import views

app_name = 'wiki'
urlpatterns = [
    path("", views.index, name="index"),
    path("wiki/<str:name>", views.pages, name="pages"),
    path("createpage", views.createpage, name="createpage"),
    path("wiki/<str:name>/edit", views.editpage, name="editpage")   
]
