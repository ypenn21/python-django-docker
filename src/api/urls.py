from django.urls import path
from api import views

urlpatterns = [
    path("", views.api, name="api"),
    path('llm/', views.getLLM, name='get_llm'),
]
