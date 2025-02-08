from django.urls import path

from pages import views

app_name = 'pages'

urlpatterns = [
    path("", views.home, name="home"),
    path("terraform.html/", views.terraform, name="terraform"),
    path("books.html/", views.books, name="book")
]
