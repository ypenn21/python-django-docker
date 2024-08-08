from django.urls import path

from pages import views

app_name = 'pages'

urlpatterns = [
    path("", views.home, name="home"),
    path("terraform.html/", views.books, name="terraform"),
]
