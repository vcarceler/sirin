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
            response += "\nRequest updated"
            old_request.datetime = timezone.now()
            old_request.processed = False
            old_request.save()
        else:
            response += "\nNo need to update request"

    except Request.DoesNotExist:
        # Si no existe una solicitud para este host la registramos
        new_request = Request(address=address, datetime=timezone.now(), processed=False)
        new_request.save()

    return HttpResponse(response)

def hosts(request):

    response = "Hosts para incluir en el playbook: "

    for r in Request.objects.filter(processed=False):
        r.processed=True
        r.save()
        response += r.address + ","

    return HttpResponse(response)