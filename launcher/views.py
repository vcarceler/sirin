from django.conf import settings
from django.http import HttpResponse
from django.shortcuts import render

# Create your views here.
def index(request):
    address=request.META['REMOTE_ADDR']

    response = "Request from: " + address
    response += "\nEXCLUSION_PERIOD: " + str(settings.EXCLUSION_PERIOD)
    return HttpResponse(response)
