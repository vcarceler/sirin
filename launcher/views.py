from django.conf import settings
from django.http import HttpResponse
from django.shortcuts import render
from django.utils import timezone

from launcher.models import Request

# Create your views here.
def index(request):
    address=request.META['REMOTE_ADDR']

    response = "Request from: " + address

    try:
        old_request = Request.objects.get(address=address)
        response += "\nOld request: " + str(old_request)

        if old_request.need_update():
            response += "\nActualizo datetime"
            old_request.datetime = timezone.now()
            old_request.save()
        else:
            response += "\nNo actualizo datetime"


    except Request.DoesNotExist:
        # Si no existe una solicitud para este host la registramos
        new_request = Request(address=address, datetime=timezone.now())
        new_request.save()

    return HttpResponse(response)
