from django.conf.urls import url
from . import views
from django.contrib.auth.views import login, logout

urlpatterns = [
    # ex: /
    url(r'^$', views.index, name='index'),
    url(r'^users/(?P<user_id>[0-9]+)/$', views.user_details, name='user_details'),
    url(r'^login/', login, name='login', kwargs={
        'template_name': 'core/login.html',
    }),
    url(r'^logout/', logout, name="logout", kwargs={
        'next_page': '/logged_out'
    }),
    url(r'^registration/', views.RegistrationView.as_view(), name='registration'),
    url(r'^logged_out/', views.logged_out, name='logged_out'),
]
