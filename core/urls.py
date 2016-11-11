from django.conf.urls import url
from django.contrib.auth.decorators import login_required

from application.settings import LOGIN_URL
from . import views
from django.contrib.auth.views import login, logout

urlpatterns = [
    # ex: /
    url(r'^$', views.index, name='index'),
    url(r'^users/(?P<pk>[0-9]+)/$', views.UserDetailsView.as_view(), name='user_details'),
    url(r'^user_edit/$', login_required(views.EditUserView.as_view(), login_url=LOGIN_URL), name='user_edit'),
    url(r'^login/', login, name='login', kwargs={
        'template_name': 'core/login.html',
    }),
    url(r'^logout/', logout, name="logout", kwargs={
        'next_page': '/logged_out'
    }),
    url(r'^registration/', views.RegistrationView.as_view(), name='registration'),
    url(r'^logged_out/', views.logged_out, name='logged_out'),
]
