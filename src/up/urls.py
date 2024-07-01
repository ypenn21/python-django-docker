from django.urls import path

from up import views

urlpatterns = [
    path("", views.up, name="up"),
    path("status", views.status, name="status"),  # Add this line

]
