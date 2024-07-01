from django.conf import settings
from django.contrib import admin
from django.urls import include
from django.urls import path

urlpatterns = [
    path("up/", include("up.urls")),
    path("", include("pages.urls")),
    path("admin/", admin.site.urls),
]
# if not settings.TESTING:
#     urlpatterns = [
#         *urlpatterns,
#         path("__debug__/", include("debug_toolbar.urls")),
#     ]
