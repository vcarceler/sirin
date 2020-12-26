from django.http import HttpResponse
from django.shortcuts import render

# Create your views here.
def index(request):
    host=request.get_host()
    address=request.META['REMOTE_ADDR']
    return HttpResponse("Host: " + host + " Address: " + address)