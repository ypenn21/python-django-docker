from django.http import HttpResponse
from src.services.llm_service import LLMService
from src.services.dao_service import DAOService
from src.services.prompt_service import PromptService
import urllib.parse
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
        param = urllib.parse.unquote(param)
        results = dao.findBook(param)
        return HttpResponse(results)
    else:
        return HttpResponse("Title parameter is missing", status=404)

def get_analysis(request):
    dao = DAOService()
    prompt = PromptService.formatPromptBookKeywords(keywords=['love', 'animals', 'coming of age'])
    character_limit = 500
    title = request.GET.get('title')
    author_name = request.GET.get('author_name')
    # prompt = request.GET.get('prompt')
    if title and author_name:
        param = urllib.parse.unquote(title)
        book_title = param
        results = dao.promptForBooks(prompt, book=book_title, author=author_name, characterLimit=character_limit)
        book_pages = [{"page": result.get("page")} for result in results]
        # Define keywords for analysis
        keywords = ["love", "romance", "relationship"]
        # Format the prompt using LLMService
        formatted_prompt = PromptService.formatPromptBookAnalysis(
            book={"book": book_title, "author": author_name},
            book_pages=book_pages,
            keywords=keywords
        )
        print(formatted_prompt)
        #TODO create prompt llm and prompt with formatted_prompt
        return HttpResponse(results)
    else:
        return HttpResponse("Title parameter is missing", status=404)

def list_llms(request):
    return HttpResponse("")