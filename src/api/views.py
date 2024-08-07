from django.http import HttpResponse
from .llm_service import LLMService
from .dao_service import DAOService
import urllib.parse
from django.http import JsonResponse
import os

def api(request):
    return HttpResponse("okay")

def test_clients(request):
    dao = DAOService()
    llm = LLMService()
    return HttpResponse("connection successful")

def get_book(request):
    dao = DAOService()
    param = request.GET.get('title')
    if param:
        results = dao.findBook(param)
        return HttpResponse(results)
    else:
        return HttpResponse("Title parameter is missing", status=404)

def list_llms(request):
    return HttpResponse("")