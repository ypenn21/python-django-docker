from src.services.llm_service import LLMService
from src.services.dao_service import DAOService
from src.services.prompt_service import format_prompt_book_keywords, format_prompt_book_analysis
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
def post_analysis(request):
    if request.method == 'POST':
        try:
            dao = DAOService()
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

                formatted_prompt = format_prompt_book_analysis(
                    book={"book": book_title, "author": author_name},
                    book_pages=book_pages,
                    keywords=keywords
                )
                print(formatted_prompt)
                # TODO create prompt llm and prompt with formatted_prompt
                return JsonResponse(results, safe=False)
            else:
                return HttpResponse("Missing required parameters", status=400)
        except json.JSONDecodeError:
            return HttpResponse("Invalid JSON payload", status=400)
    else:
        return HttpResponse("Method not allowed", status=405)

def list_llms(request):
    return HttpResponse("")