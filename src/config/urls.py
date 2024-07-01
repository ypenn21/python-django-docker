from django.conf import settings
from django.contrib import admin
from django.urls import include
from django.urls import path

urlpatterns = [
    path("up/", include("up.urls")),
    path("", include("pages.urls")),
    path("admin/", admin.site.urls),
    path("api/", include("api.urls")),
]
