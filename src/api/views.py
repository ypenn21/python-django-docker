from django.http import HttpResponse


# redis = Redis.from_url(settings.REDIS_URL)


def api(request):
    return HttpResponse("okay")
