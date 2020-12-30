from django.conf import settings
from django.http import HttpResponse
from django.shortcuts import render
from django.utils import timezone

from launcher.models import Request

# Create your views here.
def index(request):
    address=request.META['REMOTE_ADDR']

    response = "Request from: " + address

    if 'label' in request.GET:
        rlabel = request.GET['label']
    else:
        rlabel = 'default'

    try:
        old_request = Request.objects.get(address=address)
        response += " Old request: " + str(old_request)

        if old_request.need_update():
            old_request.datetime = timezone.now()
            old_request.processed = False
            old_request.label = rlabel
            old_request.save()
            response += " Request updated."
        else:
            response += " No need to update request."

    except Request.DoesNotExist:
        # Si no existe una solicitud para este host la registramos
        new_request = Request(address=address, datetime=timezone.now(), processed=False, label=rlabel)
        new_request.save()

    return HttpResponse(response)

def hosts(request):
    response = "Hosts para incluir en el playbook: "

    for r in Request.objects.filter(processed=False):
        r.processed=True
        r.save()
        response += r.address + ","

    return HttpResponse(response)