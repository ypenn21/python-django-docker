from django.http import HttpResponse
from src.services.utils_service import generate_random_number  # Import from utils_service.py
def up(request):
    return HttpResponse("okay")


def status(request):
    random_number = generate_random_number(1, 1000)  # Generate a random number between 1 and 1000
    return HttpResponse(f"okay: {random_number}")
