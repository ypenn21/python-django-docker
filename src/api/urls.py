from django.urls import path
from api import views


app_name = 'api'

urlpatterns = [
    path("", views.api, name="api"),
    path('llm/', views.list_llms, name='get_llm'),
]
