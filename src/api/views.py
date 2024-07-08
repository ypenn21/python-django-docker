from django.http import HttpResponse
from .llm_service import LLMService
import os

def api(request):
    return HttpResponse("okay")

def getLLM(request):
    """
    Retrieves a random LLM name from Vertex AI Managed AI Service.
    """
    project_id = os.getenv('GOOGLE_CLOUD_PROJECT_ID', 'next24-genai-app')
    region = os.getenv('GOOGLE_CLOUD_REGION', 'us-central1')

    llm_service = LLMService(project_id, region)
    try:
        llms = llm_service.get_llms()
        return HttpResponse(llms)
    except ValueError as e:
        return HttpResponse(f"Error: {e}", status=500)