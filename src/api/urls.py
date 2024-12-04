from django.urls import path
from api import views


app_name = 'api'

urlpatterns = [
    path("", views.api, name="api"),
    path('test_clients/', views.test_clients, name='clients'),
    path('llm/', views.list_llms, name='llm'),
    path('books/', views.get_book, name='books'),
    path('analysis', views.post_analysis, name='analysis'),
    path('document/embeddings', views.insert_book, name='insert_book'),
]
