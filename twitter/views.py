from ratelimit.exceptions import Ratelimited
from django.http.response import HttpResponse, HttpResponseForbidden
from django.shortcuts import render


def handler403(request, exception=None):
    if isinstance(exception, Ratelimited):
        return HttpResponse('You can only send one Tweet per 5 seconds', status=429)
    return HttpResponseForbidden()

def handler404(request, exception=None):
    return render(request, 'special/404.html')