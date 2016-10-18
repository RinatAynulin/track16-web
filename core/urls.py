from django.conf.urls import url
from . import views

urlpatterns = [
    # ex: /
    url(r'^$', views.index, name='index'),
    url(r'^users/(?P<user_id>[0-9]+)/$', views.user_details, name='user_details'),
]
