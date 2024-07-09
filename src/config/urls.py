from django.conf import settings
from django.contrib import admin
from django.urls import include
from django.urls import path

urlpatterns = [
    path("up/", include("up.urls", namespace='up')),
    path("", include("pages.urls", namespace='pages')),
    path("admin/", admin.site.urls),
    path("api/", include("api.urls", namespace='api')),
]
