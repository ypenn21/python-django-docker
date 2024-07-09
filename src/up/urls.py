from django.urls import path

from up import views

app_name = 'up'

urlpatterns = [
    path("", views.up, name="up"),
    path("status", views.status, name="status"),  # Add this line

]
