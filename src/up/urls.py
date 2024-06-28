from django.urls import path

from up import views

urlpatterns = [
    path("", views.index, name="index"),
    path("status", views.status, name="status"),  # Add this line

]
