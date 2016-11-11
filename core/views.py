from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse, Http404
from django.template import loader
from django.conf import settings
from django.contrib.auth import get_user_model
from django.views.generic import CreateView, UpdateView
from django.urls import reverse
from django.views.generic import DetailView

from .models import User
from .forms import RegistrationForm


def index(request):
    return redirect('posts:index')

def logged_out(request):
    return render(request, 'core/logged_out.html')


class UserDetailsView(DetailView):
    model = User
    template_name = 'core/user_details.html'
    context_object_name = 'current_user'

class RegistrationView(CreateView):
    model = User
    template_name = 'core/registration.html'
    form_class = RegistrationForm
    success_url = 'core:login'

    def get_success_url(self):
        return reverse(self.success_url)


class EditUserView(UpdateView):
    model = User
    template_name = 'core/edit_user.html'

    fields = ('username',
              'email',
              )

    def get_object(self, queryset=None):
        return get_object_or_404(User, pk=self.request.user.pk)

    def get_success_url(self):
        return reverse('core:user_details', kwargs=({'user_id': self.object.id}))
