from django.conf import settings
from django.http import HttpResponse
from django.shortcuts import render
from django.template import loader
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
        #response += " Old request: " + str(old_request)

        if old_request.need_update():
            old_request.datetime = timezone.now()
            old_request.processed = False
            old_request.label = rlabel
            old_request.save()

    except Request.DoesNotExist:
        # Si no existe una solicitud para este host la registramos
        new_request = Request(address=address, datetime=timezone.now(), processed=False, label=rlabel)
        new_request.save()

    return HttpResponse(response)

def listpendingrequests(request):
    request_list = Request.objects.filter(processed=False)
    template = loader.get_template('launcher/listpendingrequests.html')
    context = {
        'request_list': request_list,
    }

    return HttpResponse(template.render(context, request))