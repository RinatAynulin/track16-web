from django.shortcuts import render
from django.http import HttpResponse, Http404
from django.template import loader
from django.conf import settings
from django.contrib.auth import get_user_model
from django.views.generic import CreateView

from .models import User
from .forms import RegistrationForm
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

def logged_out(request):
    template = loader.get_template('core/logged_out.html')
    return HttpResponse(template.render(request))


class RegistrationView(CreateView):
    model = User
    template_name = 'core/registration.html'
    form_class = RegistrationForm
    success_url = 'core:login'

    def get_success_url(self):
        from django.urls import reverse
        return reverse(self.success_url)