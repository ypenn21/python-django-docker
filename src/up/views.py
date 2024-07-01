from django.conf import settings
from django.db import connection
from django.http import HttpResponse
from redis import Redis
from .utils import generate_random_number  # Import from utils.py


# redis = Redis.from_url(settings.REDIS_URL)


def up(request):
    return HttpResponse("okay")


# def databases(request):
#     redis.ping()
#     connection.ensure_connection()
#
#     return HttpResponse("")


def status(request):
    random_number = generate_random_number(1, 1000)  # Generate a random number between 1 and 1000
    return HttpResponse(f"I am okay {random_number}")
