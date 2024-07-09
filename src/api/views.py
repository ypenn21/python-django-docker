from django.http import HttpResponse
from .llm_service import LLMService
from django.http import JsonResponse
import os

def api(request):
    return HttpResponse("okay")

def list_llms(request):
    return HttpResponse("")