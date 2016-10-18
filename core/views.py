from django.shortcuts import render
from django.http import HttpResponse, Http404
from django.template import loader
from django.conf import settings
from django.contrib.auth import get_user_model

def index(request):
    template = loader.get_template('core/index.html')
    return HttpResponse(template.render(request))

def user_details(request, user_id):
    try:
        user = get_user_model().objects.get(pk=user_id)
    except get_user_model().DoesNotExist:
        raise Http404('User does not exist')
    template = loader.get_template('core/user_details.html')
    context = {
        'user' : user
    }
    return HttpResponse(template.render(context, request))
