from src.services.llm_service import LLMService
from src.services.dao_service import DAOService
from src.services.prompt_service import format_prompt_book_keywords, tf_search_query, get_sorted_pages
from django.http import HttpResponse, JsonResponse
from django.views.decorators.csrf import csrf_exempt
import urllib.parse
import os
import json
def api(request):
    return HttpResponse("okay")

def test_clients(request):
    dao = DAOService()
    llm = LLMService()
    return HttpResponse("connection successful")


def get_llm_service():
    project_id = os.getenv("GOOGLE_CLOUD_PROJECT_ID", "genai-playground24")
    region = os.getenv("GOOGLE_CLOUD_REGION", "us-central1")
    model = os.getenv("LLM_MODEL", "google/gemini-2.5-flash")
    return LLMService(project_id=project_id, region=region, model=model)

llm_service=get_llm_service()

def get_book(request):
    dao = DAOService()
    param = request.GET.get('title')
    if param:
        param = urllib.parse.unquote(param)
        results = dao.find_book(param)
        return HttpResponse(results)
    else:
        return HttpResponse("Title parameter is missing", status=404)
        
@csrf_exempt
def post_analysis(request, dao=DAOService()):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            book_title = data.get("book")
            author_name = data.get("author")
            keywords = data.get("keyWords")

            if book_title and author_name and keywords:
                character_limit = 500
                results = dao.prompt_for_books(
                    format_prompt_book_keywords(keywords),
                    book=book_title,
                    author=author_name,
                    characterLimit=character_limit
                )
                book_pages = [{"page": result.get("page")} for result in results]

                analysis = llm_service.analysis_book(
                    book_title, author_name,
                    book_pages=book_pages,
                    keywords=keywords
                )
                return HttpResponse(analysis)
            else:
                return HttpResponse("Missing required parameters", status=400)
        except json.JSONDecodeError:
            return HttpResponse("Invalid JSON payload", status=400)
    else:
        return HttpResponse("Method not allowed", status=405)

@csrf_exempt
def tf_transform(request, dao=DAOService()):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            script = data.get("script")

            if script:
                character_limit = 500
                results = dao.prompt_for_books(
                    tf_search_query(),
                    characterLimit=character_limit
                )
                # book_pages = [{"page": result.get("page")} for result in results]
                # context = " ".join([page.get("page") for page in book_pages])
                context = get_sorted_pages(results)
                analysis = llm_service.tf_transform(
                    script, context)
                return HttpResponse(analysis)
            else:
                return HttpResponse("Missing required parameters", status=400)
        except json.JSONDecodeError:
            return HttpResponse("Invalid JSON payload", status=400)
    else:
        return HttpResponse("Method not allowed", status=405)

def list_llms(request):
    """
    Retrieves a list of available LLMs from Vertex AI.

    Args:
        request: The HTTP request object.

    Returns:
        A JSON response containing a list of LLM names.
    """
    llms = llm_service.list_llms()

    return JsonResponse({"llms": llms})

@csrf_exempt
def insert_book(request, dao = DAOService()):
    if request.method == 'POST':
        try:
            body = json.loads(request.body)
            headers = request.headers

            # Validate headers (replace with your actual validation logic)
            error_msg = validate_request(body, headers)  # Placeholder for validation function
            if error_msg:
                return JsonResponse({"error": error_msg}, status=400)

            book_title = body.get("book")
            author_name = body.get("author")

            author_id = dao.insert_author(bio="famous author", author=author_name)

            dao.insert_book(author_id=author_id, title=book_title, public_private="public", year="2000-01-01")

            return JsonResponse({"status": 200}, status=200)  # Adjust status codes as needed


        except json.JSONDecodeError:
            return JsonResponse({"error": "Invalid JSON payload"}, status=400)

    else:
        return JsonResponse({"error": "Method not allowed"}, status=405)



def validate_request(body, headers):
    """
    Placeholder for request validation logic.  Replace with your actual validation.
    """
    # Check for required headers and body content
    # Example:
    if not headers.get("Content-Type") == "application/json":
         return "Invalid Content-Type header"
    book_title = body.get("book")
    author_name = body.get("author")
    if not book_title or not author_name:
        return "Missing 'name' in the request body."
